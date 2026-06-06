import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import Project
from datetime import datetime
from .forms import ProjectForm

def dashboard(request):
    all_projects = Project.objects.all()
    return render(request, 'projects/dashboard.html', {'projects': all_projects})

def upload_csv(request):
    if request.method == "POST" and request.FILES.get('csv_file'):
        uploaded_file = request.FILES['csv_file']
        file_name = uploaded_file.name.lower()
        
        try:
            if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
                df = pd.read_excel(uploaded_file)
            elif file_name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                messages.error(request, "Unsupported file format.")
                return redirect('dashboard')
            
            df.columns = df.columns.str.strip()
            df = df.dropna(subset=['Project / Topic'])
            
            for index, row in df.iterrows():
                project_name = str(row['Project / Topic']).strip()
                if not project_name or project_name == "nan" or project_name.startswith(',,,'):
                    continue
                
                last_updated_val = row.get('Last Updated')
                parsed_date = None
                if pd.notna(last_updated_val) and str(last_updated_val).strip():
                    if isinstance(last_updated_val, datetime):
                        parsed_date = last_updated_val.date()
                    else:
                        try:
                            parsed_date = datetime.strptime(str(last_updated_val).strip(), '%Y-%m-%d').date()
                        except ValueError:
                            pass
                
                main_link = str(row.get('Main File / Folder Link', '')) if pd.notna(row.get('Main File / Folder Link')) else ''
                notes_link = str(row.get('Notes Link', '')) if pd.notna(row.get('Notes Link')) else ''
                combined_links = f"Folder: {main_link}\nNotes: {notes_link}".strip()

                Project.objects.update_or_create(
                    name=project_name,
                    defaults={
                        'category': str(row.get('Category', '')) if pd.notna(row.get('Category')) else '',
                        'project_type': str(row.get('Type', '')) if pd.notna(row.get('Type')) else '',
                        'priority': str(row.get('Priority', '')) if pd.notna(row.get('Priority')) else '',
                        'status': str(row.get('Status', '')) if pd.notna(row.get('Status')) else '',
                        'last_updated': parsed_date,
                        'summary': str(row.get('Summary', '')) if pd.notna(row.get('Summary')) else '',
                        'links': combined_links,
                        
                        # Mapping the new columns here
                        'ai_source': str(row.get('AI Source', '')) if pd.notna(row.get('AI Source')) else '',
                        'ai_prompt_link': str(row.get('AI Prompt Link', '')) if pd.notna(row.get('AI Prompt Link')) else '',
                        'related_websites': str(row.get('Related Websites', '')) if pd.notna(row.get('Related Websites')) else '',
                        
                        'tags': str(row.get('Tags', '')) if pd.notna(row.get('Tags')) else '',
                    }
                )
            
            messages.success(request, "Master sheet synchronized successfully with all columns!")
            
        except Exception as e:
            messages.error(request, f"Error processing file: {e}")
            
        return redirect('dashboard')
        
    return redirect('dashboard')

def export_csv(request):
    projects = Project.objects.all()
    data = []
    for p in projects:
        main_link = ""
        notes_link = ""
        if p.links:
            lines = p.links.split('\n')
            for line in lines:
                if line.startswith("Folder: "):
                    main_link = line.replace("Folder: ", "")
                elif line.startswith("Notes: "):
                    notes_link = line.replace("Notes: ", "")

        data.append({
            'Project / Topic': p.name,
            'Category': p.category,
            'Type': p.project_type,
            'Priority ': p.priority,
            'Status ': p.status,
            'Last Updated ': p.last_updated.strftime('%Y-%m-%d') if p.last_updated else '',
            'Summary ': p.summary,
            'Main File / Folder Link ': main_link,
            'Notes Link': notes_link,
            
            # Exporting the new columns back to the Excel output format
            'AI Source': p.ai_source,
            'AI Prompt Link ': p.ai_prompt_link,
            'Related Websites ': p.related_websites,
            
            'Tags': p.tags
        })
    
    df = pd.DataFrame(data)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Master_Data_Sheet_Updated.csv"'
    df.to_csv(path_or_buf=response, index=False)
    return response

def project_detail(request, pk):
    # Fetch the exact project using its ID, or show a 404 error page if it doesn't exist
    project = get_object_or_404(Project, pk=pk)
    
    # Send that project data to HTML template
    return render(request, 'projects/project_detail.html', {'project': project})
    
    if request.method == "POST":
        if 'update_project' in request.POST:
            project.status = request.POST.get('status', '').strip()
            project.priority = request.POST.get('priority', '').strip()
            project.summary = request.POST.get('summary', '').strip()
            project.links = request.POST.get('links', '').strip()
            
            # Save entries from the new editing fields
            project.ai_source = request.POST.get('ai_source', '').strip()
            project.ai_prompt_link = request.POST.get('ai_prompt_link', '').strip()
            project.related_websites = request.POST.get('related_websites', '').strip()
            
            project.tags = request.POST.get('tags', '').strip()
            project.last_updated = datetime.now().date()
            project.save()
            messages.success(request, f"Changes to '{project.name}' saved successfully!")
            
        elif 'add_log' in request.POST:
            from .models import StudyLog
            duration = request.POST.get('duration_minutes', 0)
            notes = request.POST.get('notes', '').strip()
            if duration and notes:
                StudyLog.objects.create(
                    project=project,
                    duration_minutes=int(duration),
                    notes=notes
                )
                project.last_updated = datetime.now().date()
                project.save()
                messages.success(request, "Study session logged successfully!")
                
        return redirect('project_detail', project_id=project.id)

    logs = project.logs.all().order_by('-date_logged')
    return render(request, 'projects/project_detail.html', {'project': project, 'logs': logs})

def edit_project(request, pk):
    # 1. Fetch the specific project using its unique ID (pk)
    project = get_object_or_404(Project, pk=pk)
    
    # 2. Check if the user clicked the "Save Changes" button (POST request)
    if request.method == 'POST':
        # Bind the form to the incoming data and link it to our existing project
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()  # Saves all 11 columns back to the database!
            return redirect('project_detail', pk=project.pk)  # Go back to the detail view
            
    # 3. If they just arrived at the page normally (GET request)
    else:
        # Pre-fill the form fields with the current project data
        form = ProjectForm(instance=project)
        
    # 4. Send the form and the project data to the HTML template
    return render(request, 'projects/edit_project.html', {'form': form, 'project': project})

def delete_project(request, pk):
    # Fetch the specific project or fail with a 404
    project = get_object_or_404(Project, pk=pk)
    
    # If they click "Confirm Delete", it sends a POST request
    if request.method == 'POST':
        project.delete() # Deletes it from the database completely!
        return redirect('dashboard') # Send them safely back to the main dashboard
        
    # If they just land on the page, show the confirmation screen
    return render(request, 'projects/delete_confirm.html', {'project': project})