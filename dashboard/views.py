from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Sum, Avg
from django.db import connection
from datetime import datetime, timedelta

def dashboard_home(request):
    """Render the main dashboard page"""
    return render(request, 'dashboard/index.html')

def get_chart_data(request):
    """API endpoint to fetch chart data"""
    chart_type = request.GET.get('chart_type', 'default')
    
    if chart_type == 'user_activity':
        timeframe = request.GET.get('timeframe', 'monthly')
        
        # Adjust query based on timeframe
        if timeframe == 'weekly':
            days = 7
            group_format = '%Y-%m-%d'  # Daily for a week
        elif timeframe == 'yearly':
            days = 365
            group_format = '%Y-%m'     # Monthly for a year
        else:  # monthly (default)
            days = 30
            group_format = '%Y-%m-%d'  # Daily for a month
        
        # Consulta para obtener actividad de encuestas
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM encuestas")
            total_encuestas = cursor.fetchone()[0] or 0
            
        # Generar datos distribuidos en el período seleccionado
        if timeframe == 'weekly':
            labels = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7, 0, -1)]
            data = [int(total_encuestas * 0.05 * (i+1)) for i in range(7)]
        elif timeframe == 'yearly':
            labels = [(datetime.now() - timedelta(days=30*i)).strftime('%Y-%m') for i in range(12, 0, -1)]
            data = [int(total_encuestas * 0.08 * (i+1)) for i in range(12)]
        else:  # monthly
            labels = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30, 0, -1)]
            data = [int(total_encuestas * 0.03 * ((i % 7) + 1)) for i in range(30)]
        
        return JsonResponse({
            'labels': labels,
            'datasets': [{
                'label': 'Actividad de Encuestas',
                'data': data,
                'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                'borderColor': 'rgba(54, 162, 235, 1)',
                'borderWidth': 1
            }]
        })
    
    elif chart_type == 'category_distribution':
        # Consulta para distribución por tipo de sustancia
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 'Alcohol' as categoria, COUNT(*) as count FROM alcohol
                UNION ALL
                SELECT 'Tabaco' as categoria, COUNT(*) as count FROM tabaco
                UNION ALL
                SELECT 'Marihuana' as categoria, COUNT(*) as count FROM marihuana
                UNION ALL
                SELECT 'Cocaína' as categoria, COUNT(*) as count FROM cocaina
                UNION ALL
                SELECT 'Heroína' as categoria, COUNT(*) as count FROM heroína
                UNION ALL
                SELECT 'Éxtasis' as categoria, COUNT(*) as count FROM extasis
                UNION ALL
                SELECT 'Basuco' as categoria, COUNT(*) as count FROM basuco
                UNION ALL
                SELECT 'Inhalables' as categoria, COUNT(*) as count FROM inhalables
                UNION ALL
                SELECT 'Estimulantes' as categoria, COUNT(*) as count FROM estimulantes
                UNION ALL
                SELECT 'Tranquilizantes' as categoria, COUNT(*) as count FROM tranquilizantes
            """)
            rows = cursor.fetchall()
            
        labels = [row[0] for row in rows]
        data = [row[1] for row in rows]
        
        return JsonResponse({
            'labels': labels,
            'datasets': [{
                'data': data,
                'backgroundColor': ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b', '#5a5c69', '#6f42c1', '#fd7e14', '#20c997', '#6c757d'],
                'hoverBackgroundColor': ['#2e59d9', '#17a673', '#2c9faf', '#dda20a', '#be2617', '#3a3b45', '#5a32a3', '#d96b12', '#17a47a', '#5a6268'],
                'hoverBorderColor': "rgba(234, 236, 244, 1)",
            }]
        })
    
    elif chart_type == 'yearly_comparison':
        # Obtener datos de comparación entre diferentes sustancias
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 'Legales' as tipo, 
                (SELECT COUNT(*) FROM alcohol) + (SELECT COUNT(*) FROM tabaco) as count
                UNION ALL
                SELECT 'Ilegales' as tipo, 
                (SELECT COUNT(*) FROM marihuana) + (SELECT COUNT(*) FROM cocaina) + 
                (SELECT COUNT(*) FROM heroína) + (SELECT COUNT(*) FROM extasis) + 
                (SELECT COUNT(*) FROM basuco) + (SELECT COUNT(*) FROM inhalables) as count
            """)
            tipos_sustancias = cursor.fetchall()
        
        # Convertir a formato para gráfico de comparación
        labels = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        
        # Distribuir los conteos a lo largo de los meses (simulación)
        legales_total = tipos_sustancias[0][1] if len(tipos_sustancias) > 0 else 0
        ilegales_total = tipos_sustancias[1][1] if len(tipos_sustancias) > 1 else 0
        
        # Generar datos distribuidos por mes
        legales_data = [int(legales_total/12 * (0.7 + 0.6 * (i % 3))) for i in range(12)]
        ilegales_data = [int(ilegales_total/12 * (0.5 + 0.7 * ((i+1) % 3))) for i in range(12)]
        
        return JsonResponse({
            'labels': labels,
            'datasets': [
                {
                    'label': 'Sustancias Legales',
                    'backgroundColor': '#4e73df',
                    'data': legales_data
                },
                {
                    'label': 'Sustancias Ilegales',
                    'backgroundColor': '#1cc88a',
                    'data': ilegales_data
                }
            ]
        })
    
    elif chart_type == 'monthly_trend':
        # Consulta para tendencia mensual de registros
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) as total FROM personas
            """)
            total_personas = cursor.fetchone()[0] or 0
        
        # Crear datos de tendencia mensual (simulación)
        monthly_data = [int(total_personas/12 * (0.5 + 0.8 * ((i+1) % 4) / 3)) for i in range(12)]
        
        month_abbr = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
                      'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        
        return JsonResponse({
            'labels': month_abbr,
            'datasets': [{
                'label': 'Tendencia Mensual',
                'data': monthly_data,
                'backgroundColor': 'rgba(28, 200, 138, 0.05)',
                'borderColor': 'rgba(28, 200, 138, 1)',
                'pointRadius': 3,
                'pointBackgroundColor': 'rgba(28, 200, 138, 1)',
                'pointBorderColor': 'rgba(28, 200, 138, 1)',
                'pointHoverRadius': 5,
                'pointHoverBackgroundColor': 'rgba(28, 200, 138, 1)',
                'pointHoverBorderColor': 'rgba(28, 200, 138, 1)',
                'pointHitRadius': 10,
                'pointBorderWidth': 2,
                'tension': 0.3,
                'fill': True
            }]
        })
    
    # Default response for invalid chart type
    return JsonResponse({'error': 'Invalid chart type'}, status=400)

def get_summary_data(request):
    """API endpoint to fetch summary data for dashboard cards"""
    try:
        # Consultas para obtener datos de resumen
        with connection.cursor() as cursor:
            # Total de personas encuestadas
            cursor.execute("SELECT COUNT(*) FROM personas")
            total_personas = cursor.fetchone()[0] or 0
            
            # Total de registros de sustancias
            cursor.execute("""
                SELECT 
                    (SELECT COUNT(*) FROM alcohol) +
                    (SELECT COUNT(*) FROM tabaco) +
                    (SELECT COUNT(*) FROM marihuana) +
                    (SELECT COUNT(*) FROM cocaina) +
                    (SELECT COUNT(*) FROM heroína) +
                    (SELECT COUNT(*) FROM extasis) +
                    (SELECT COUNT(*) FROM basuco) +
                    (SELECT COUNT(*) FROM inhalables) +
                    (SELECT COUNT(*) FROM estimulantes) +
                    (SELECT COUNT(*) FROM tranquilizantes) as total
            """)
            total_sustancias = cursor.fetchone()[0] or 0
            
            # Promedio de sustancias por persona
            average_value = round(total_sustancias / total_personas, 2) if total_personas > 0 else 0
            
            # Porcentaje de personas con al menos una sustancia
            cursor.execute("""
                SELECT COUNT(DISTINCT DIRECTORIO) FROM (
                    SELECT DIRECTORIO FROM alcohol
                    UNION
                    SELECT DIRECTORIO FROM tabaco
                    UNION
                    SELECT DIRECTORIO FROM marihuana
                    UNION
                    SELECT DIRECTORIO FROM cocaina
                    UNION
                    SELECT DIRECTORIO FROM heroína
                    UNION
                    SELECT DIRECTORIO FROM extasis
                    UNION
                    SELECT DIRECTORIO FROM basuco
                    UNION
                    SELECT DIRECTORIO FROM inhalables
                    UNION
                    SELECT DIRECTORIO FROM estimulantes
                    UNION
                    SELECT DIRECTORIO FROM tranquilizantes
                )
            """)
            personas_con_sustancias = cursor.fetchone()[0] or 0
            completion_rate = round((personas_con_sustancias * 100.0) / total_personas, 1) if total_personas > 0 else 0
            
            # Personas sin registros de sustancias
            pending_items = total_personas - personas_con_sustancias
        
        return JsonResponse({
            'total_records': total_personas,
            'average_value': average_value,
            'completion_rate': completion_rate,
            'pending_items': pending_items
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'total_records': 0,
            'average_value': 0,
            'completion_rate': 0,
            'pending_items': 0
        })
