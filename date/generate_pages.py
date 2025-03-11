import os
import json
from datetime import datetime, timedelta

def load_calculator_data():
    with open('../calculators.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        date_category = next((c for c in data['categories'] if c['name'] == 'Date'), None)
        if date_category:
            return {
                "variations": [
                    {
                        "id": "1-week-from-today",
                        "name": "1 Week From Today",
                        "description": "Calculate the date exactly one week from today",
                        "keywords": ["week", "7 days", "next week", "future date"],
                        "relatedContent": [
                            "Plan weekly meetings and events",
                            "Schedule follow-up appointments",
                            "Set short-term deadlines",
                            "Plan weekly routines"
                        ]
                    },
                    {
                        "id": "2-weeks-from-today",
                        "name": "2 Weeks From Today",
                        "description": "Find the date two weeks from today",
                        "keywords": ["2 weeks", "14 days", "biweekly", "fortnight"],
                        "relatedContent": [
                            "Plan biweekly meetings",
                            "Schedule follow-ups",
                            "Set project milestones",
                            "Plan workout routines"
                        ]
                    }
                ],
                "template": {
                    "nameTemplate": "{n} Weeks From Today",
                    "descriptionTemplate": "Calculate the date {n} weeks from today",
                    "keywords": ["weeks", "future date", "planning", "schedule"],
                    "relatedContent": [
                        "Long-term planning",
                        "Project deadlines",
                        "Event scheduling",
                        "Future date calculations"
                    ]
                }
            }
    return None

def get_calculator_data(weeks, calculator_data):
    # Check if it's a predefined variation
    if calculator_data:
        variation = next((v for v in calculator_data['variations'] if v['id'] == f"{weeks}-week{'s' if weeks > 1 else ''}-from-today"), None)
        if variation:
            return variation
        
        # Use template for other weeks
        template = calculator_data['template']
        return {
            "name": template['nameTemplate'].replace('{n}', str(weeks)),
            "description": template['descriptionTemplate'].replace('{n}', str(weeks)),
            "keywords": template['keywords'],
            "relatedContent": template['relatedContent']
        }
    
    # Fallback data if JSON not available
    return {
        "name": f"{weeks} Week{'s' if weeks > 1 else ''} From Today",
        "description": f"Calculate the date {weeks} week{'s' if weeks > 1 else ''} from today",
        "keywords": ["weeks", "future date", "planning", "schedule"],
        "relatedContent": [
            "Long-term planning",
            "Project deadlines",
            "Event scheduling",
            "Future date calculations"
        ]
    }

def generate_week_page(weeks):
    # Calculate the future date
    today = datetime.now()
    future_date = today + timedelta(weeks=weeks)
    
    # Format dates
    today_str = today.strftime("%B %d, %Y")
    future_str = future_date.strftime("%B %d, %Y")
    
    # Create page title and description
    weeks_text = "1 week" if weeks == 1 else f"{weeks} weeks"
    title = f"{weeks_text.capitalize()} From Today - Date Calculator"
    description = f"Calculate the date {weeks_text} from today ({today_str}). Find out what date will be in {weeks_text}."

    # Generate dynamic content based on weeks
    use_cases = [
        f"Plan meetings and events {weeks_text} in advance",
        f"Schedule appointments and follow-ups for {weeks_text} later",
        f"Set project milestones and deadlines",
        f"Plan future travel or events"
    ]

    planning_tips = [
        "Consider weekends and holidays when planning",
        "Set reminders a few days before the target date",
        "Account for business days vs calendar days",
        "Use digital calendar apps for better tracking"
    ]

    # Generate related weeks for navigation (4-5 related weeks)
    related_weeks = []
    current_group = (weeks - 1) // 10 * 10 + 1  # Group weeks in tens (1-10, 11-20, etc.)
    end_group = min(current_group + 9, 50)
    related_weeks = [w for w in range(current_group, end_group + 1) if w != weeks][:5]

    # Generate related calculators HTML
    related_html = []
    for w in related_weeks:
        w_text = "1 week" if w == 1 else f"{w} weeks"
        url_suffix = "week" if w == 1 else "weeks"
        related_html.append(f'''
            <a href="/date/{w}-{url_suffix}-from-today.html" 
               class="flex items-center p-4 bg-white rounded-xl shadow-sm hover:shadow-md transition-all duration-300 group">
                <div class="bg-blue-50 rounded-full p-3 mr-4 group-hover:bg-blue-100 transition-colors duration-300">
                    <i class="fas fa-calendar-alt text-blue-600 text-xl"></i>
                </div>
                <div>
                    <h3 class="font-semibold text-gray-800 group-hover:text-blue-600 transition-colors duration-300">
                        {w_text.capitalize()} from today
                    </h3>
                    <p class="text-sm text-gray-500">Calculate future date →</p>
                </div>
            </a>
        ''')

    # Generate partner calculator section only for weeks 1-16
    partner_calculator = ""
    if weeks <= 16:
        partner_calculator = f'''
            <!-- External Calculator Link -->
            <a href="https://www.calculatorvalue.com/life/weeks-from/{weeks}-{'weeks' if weeks > 1 else 'week'}-from-today" 
               class="block bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-xl p-4 hover:from-blue-600 hover:to-blue-700 transition-all duration-300">
                <div class="flex items-center justify-between">
                    <div class="flex items-center">
                        <div class="bg-white/10 rounded-full p-3 mr-4">
                            <i class="fas fa-calculator text-white text-xl"></i>
                        </div>
                        <div>
                            <h3 class="font-semibold text-lg">Try Our Advanced {weeks_text.capitalize()} Calculator</h3>
                            <p class="text-blue-100">More features and detailed results →</p>
                        </div>
                    </div>
                    <i class="fas fa-external-link-alt text-white/70"></i>
                </div>
            </a>
        '''

    # Generate the HTML content
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        .page-loader {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: #fff;
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            transition: opacity 0.3s ease-in-out;
        }}
        .page-loader.loaded {{
            opacity: 0;
            pointer-events: none;
        }}
        .main-content {{
            opacity: 0;
            transition: opacity 0.3s ease-in-out;
        }}
        .main-content.loaded {{
            opacity: 1;
        }}
    </style>
</head>
<body class="bg-gray-50">
    <!-- Loading spinner -->
    <div class="page-loader">
        <div class="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-600"></div>
    </div>

    <!-- Main content wrapper -->
    <div class="main-content">
        <div id="navbar"></div>

        <main class="py-8">
            <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
                <!-- Breadcrumb -->
                <nav class="text-gray-500 mb-4">
                    <ol class="list-none p-0 flex flex-wrap space-x-2">
                        <li><a href="/" class="hover:text-blue-600">Home</a></li>
                        <li>/</li>
                        <li><a href="/date" class="hover:text-blue-600">Date Calculators</a></li>
                        <li>/</li>
                        <li class="text-gray-900">{weeks_text.capitalize()} From Today</li>
                    </ol>
                </nav>

                <!-- Title Section -->
                <div class="text-center mb-6">
                    <h1 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-3">{weeks_text.capitalize()} From Today</h1>
                    <p class="text-lg sm:text-xl text-gray-600">Find out what date will be in {weeks_text} from today</p>
                </div>

                <!-- Enhanced Date Display -->
                <div class="bg-gradient-to-r from-blue-50 to-blue-100 rounded-2xl shadow-lg p-6 mb-6">
                    <div class="flex flex-col md:flex-row items-center justify-between gap-6">
                        <!-- Today's Date Card -->
                        <div class="w-full md:w-5/12 bg-white rounded-xl shadow-sm p-4">
                            <div class="text-center">
                                <span class="inline-block bg-blue-100 text-blue-800 text-xs font-semibold px-3 py-1 rounded-full mb-2">Today</span>
                                <div class="text-3xl font-bold text-gray-800 mb-1">{today.strftime("%B %d")}</div>
                                <div class="text-lg text-gray-600">{today.strftime("%Y")}</div>
                                <div class="text-sm text-blue-600 mt-1">{today.strftime("%A")}</div>
                            </div>
                        </div>

                        <!-- Arrow and Days -->
                        <div class="flex flex-col items-center py-2">
                            <div class="text-blue-600 font-semibold mb-1">{weeks * 7} days</div>
                            <div class="relative">
                                <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-12 h-12 bg-blue-100 rounded-full"></div>
                                <i class="fas fa-arrow-right text-blue-600 text-2xl relative z-10"></i>
                            </div>
                        </div>

                        <!-- Future Date Card -->
                        <div class="w-full md:w-5/12 bg-white rounded-xl shadow-sm p-4">
                            <div class="text-center">
                                <span class="inline-block bg-green-100 text-green-800 text-xs font-semibold px-3 py-1 rounded-full mb-2">{weeks_text.capitalize()} Later</span>
                                <div class="text-3xl font-bold text-green-600 mb-1">{future_date.strftime("%B %d")}</div>
                                <div class="text-lg text-gray-600">{future_date.strftime("%Y")}</div>
                                <div class="text-sm text-green-600 mt-1">{future_date.strftime("%A")}</div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Related Calculators and External Link - Above the fold -->
                <div class="grid gap-6 mb-8">
                    {partner_calculator}

                    <!-- Related Week Calculators -->
                    <div class="bg-gradient-to-r from-gray-50 to-blue-50 rounded-2xl p-6">
                        <h2 class="text-xl font-semibold text-gray-900 mb-4">Related Date Calculators</h2>
                        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                            {' '.join(related_html)}
                        </div>
                    </div>
                </div>

                <!-- Key Information -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
                    <div class="bg-blue-50 rounded-xl p-6">
                        <h2 class="text-xl font-semibold text-gray-900 mb-4">Time Overview</h2>
                        <ul class="space-y-3">
                            <li class="flex items-center">
                                <i class="fas fa-calendar-week text-blue-600 w-6"></i>
                                <span class="ml-2">Weeks: <strong>{weeks}</strong></span>
                            </li>
                            <li class="flex items-center">
                                <i class="fas fa-calendar-day text-blue-600 w-6"></i>
                                <span class="ml-2">Days: <strong>{weeks * 7}</strong></span>
                            </li>
                            <li class="flex items-center">
                                <i class="fas fa-clock text-blue-600 w-6"></i>
                                <span class="ml-2">Hours: <strong>{weeks * 7 * 24}</strong></span>
                            </li>
                        </ul>
                    </div>
                    <div class="bg-green-50 rounded-xl p-6">
                        <h2 class="text-xl font-semibold text-gray-900 mb-4">Date Details</h2>
                        <ul class="space-y-3">
                            <li class="flex items-center">
                                <i class="fas fa-calendar-alt text-green-600 w-6"></i>
                                <span class="ml-2">Start: <strong>{today.strftime("%A, %B %d")}</strong></span>
                            </li>
                            <li class="flex items-center">
                                <i class="fas fa-calendar-check text-green-600 w-6"></i>
                                <span class="ml-2">End: <strong>{future_date.strftime("%A, %B %d")}</strong></span>
                            </li>
                            <li class="flex items-center">
                                <i class="fas fa-calendar text-green-600 w-6"></i>
                                <span class="ml-2">Month{'s' if today.month != future_date.month else ''}: 
                                    <strong>{today.strftime("%B")}{" → " + future_date.strftime("%B") if today.month != future_date.month else ""}</strong>
                                </span>
                            </li>
                        </ul>
                    </div>
                </div>

                <!-- Comprehensive Guide -->
                <div class="bg-white rounded-xl shadow-md p-6 mb-12">
                    <h2 class="text-2xl font-semibold text-gray-900 mb-6">Complete Guide to {weeks_text.capitalize()} Date Planning</h2>
                    
                    <div class="space-y-6">
                        <!-- Understanding the Calculation -->
                        <div>
                            <h3 class="text-xl font-semibold text-gray-800 mb-3">Understanding the Calculation</h3>
                            <p class="text-gray-600 mb-4">When calculating {weeks_text} from {today_str}, we account for:</p>
                            <ul class="list-disc list-inside text-gray-600 space-y-2 ml-4">
                                <li>Regular calendar progression across {weeks * 7} days</li>
                                <li>Month transitions and varying month lengths</li>
                                <li>Year transitions when applicable</li>
                                <li>Weekend and weekday distributions</li>
                            </ul>
                        </div>

                        <!-- Common Use Cases -->
                        <div>
                            <h3 class="text-xl font-semibold text-gray-800 mb-3">Common Use Cases</h3>
                            <p class="text-gray-600 mb-4">This {weeks_text} calculator is particularly useful for:</p>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                {generate_list_items(use_cases[:4])}
                            </div>
                        </div>

                        <!-- Planning Tips -->
                        <div>
                            <h3 class="text-xl font-semibold text-gray-800 mb-3">Planning Tips</h3>
                            <p class="text-gray-600 mb-4">Make the most of your {weeks_text} planning with these tips:</p>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                {generate_list_items(planning_tips[:4])}
                            </div>
                        </div>

                        <!-- Additional Considerations -->
                        <div>
                            <h3 class="text-xl font-semibold text-gray-800 mb-3">Additional Considerations</h3>
                            <div class="bg-gray-50 rounded-lg p-4">
                                <p class="text-gray-600 mb-3">When planning {weeks_text} ahead, consider these factors:</p>
                                <ul class="list-disc list-inside text-gray-600 space-y-2 ml-4">
                                    <li>Holiday schedules and business days</li>
                                    <li>Seasonal changes and weather patterns</li>
                                    <li>Time zone differences for international planning</li>
                                    <li>Buffer time for unexpected delays</li>
                                </ul>
                            </div>
                        </div>

                        <!-- Pro Tips -->
                        <div class="bg-blue-50 rounded-lg p-6">
                            <h3 class="text-xl font-semibold text-gray-800 mb-3">Pro Tips</h3>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div class="flex items-start">
                                    <i class="fas fa-lightbulb text-yellow-500 text-xl mt-1 mr-3"></i>
                                    <p class="text-gray-700">Set reminders {weeks//2} {'week' if weeks//2 == 1 else 'weeks'} before the target date</p>
                                </div>
                                <div class="flex items-start">
                                    <i class="fas fa-calendar-alt text-blue-500 text-xl mt-1 mr-3"></i>
                                    <p class="text-gray-700">Use digital calendar apps for better tracking</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </main>

        <div id="footer"></div>
    </div>

    <script src="/js/components.js"></script>
    <script>
        // Track loading state of components
        let componentsLoaded = {{
            navbar: false,
            footer: false
        }};

        function checkAllComponentsLoaded() {{
            if (componentsLoaded.navbar && componentsLoaded.footer) {{
                // Hide loader and show content
                document.querySelector('.page-loader').classList.add('loaded');
                document.querySelector('.main-content').classList.add('loaded');
            }}
        }}

        document.addEventListener('DOMContentLoaded', async function() {{
            try {{
                await Promise.all([
                    loadComponent('navbar', '/components/navbar.html').then(() => {{
                        componentsLoaded.navbar = true;
                        checkAllComponentsLoaded();
                    }}),
                    loadComponent('footer', '/components/footer.html').then(() => {{
                        componentsLoaded.footer = true;
                        checkAllComponentsLoaded();
                    }})
                ]);
            }} catch (error) {{
                console.error('Error loading components:', error);
                document.querySelector('.page-loader').innerHTML = `
                    <div class="text-center">
                        <p class="text-red-600 mb-2">Error loading page components</p>
                        <button onclick="window.location.reload()" class="px-4 py-2 bg-blue-600 text-white rounded">
                            Retry
                        </button>
                    </div>
                `;
            }}
        }});
    </script>
</body>
</html>'''

    # Create the file
    filename = f"{weeks}-week{'s' if weeks > 1 else ''}-from-today.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)

def generate_list_items(items):
    html = []
    icons = ['calendar-check', 'clock', 'tasks', 'calendar-alt']
    for i, item in enumerate(items):
        icon = icons[i % len(icons)]
        html.append(f'''
            <div class="flex items-start">
                <i class="fas fa-{icon} text-blue-600 text-xl mt-1 mr-3"></i>
                <p class="text-gray-600">{item}</p>
            </div>
        ''')
    return '\n'.join(html)

def main():
    # Generate pages for all 50 weeks
    for weeks in range(1, 51):
        generate_week_page(weeks)
        print(f"Generated page for {weeks} week(s)")

if __name__ == "__main__":
    main()