# Dashboard Configuration

# Theme Configuration
THEME_CONFIG = {
    'primary_color': '#00ff88',
    'secondary_color': '#ff6b6b',
    'background_color': '#0e1117',
    'card_background': '#1e1e1e',
    'border_color': '#333',
    'text_color': 'white'
}

# Sample Data Configuration
SAMPLE_DATA = {
    'skills': {
        'React': 45,
        'Node.js': 38,
        'Python': 32,
        'AWS': 28,
        'TypeScript': 24,
        'Vue.js': 35,
        'Angular': 28,
        'MongoDB': 25,
        'PostgreSQL': 22
    },
    'trending_skills': {
        'TypeScript': 25,
        'Next.js': 18,
        'GraphQL': 15,
        'Tailwind CSS': 12,
        'Rust': 10
    },
    'seniority_distribution': {
        'Senior': 45,
        'Mid': 35,
        'Junior': 20
    },
    'salary_ranges': {
        'Senior': '$85-120k',
        'Mid': '$60-85k',
        'Junior': '$40-60k'
    },
    'metrics': {
        'active_jobs': 156,
        'new_this_week': 28,
        'avg_processing': '2.3d',
        'success_rate': '87%'
    }
}

# Filter Options
FILTER_OPTIONS = {
    'date_ranges': ['1 week', '2 weeks', '1 month', '3 months'],
    'role_types': ['All Roles', 'Frontend', 'Backend', 'Full Stack', 'DevOps', 'Data Science'],
    'seniority_levels': ['Junior', 'Mid', 'Senior'],
    'companies': ['All companies', 'Google', 'Microsoft', 'Amazon', 'Meta', 'Apple', 'Netflix'],
    'role_filters': ['Developer', 'Designer', 'Manager', 'Analyst']
}

# Chart Configuration
CHART_CONFIG = {
    'skills_chart': {
        'color_scale': 'Blues',
        'orientation': 'h'
    },
    'seniority_chart': {
        'hole': 0.6,
        'colors': ['#1f77b4', '#ff7f0e', '#2ca02c']
    }
}

# Update Intervals (in seconds)
UPDATE_INTERVALS = {
    'data_refresh': 120,  # 2 minutes
    'metrics_update': 60,  # 1 minute
    'chart_refresh': 300   # 5 minutes
} 