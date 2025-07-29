from sources.reddit import RedditSource
from sources.google_trends import GoogleTrendsSource
from sources.quora import QuoraSource
from sources.stack_overflow import StackOverflowSource
from sources.twitter import TwitterSource
import os
from datetime import datetime

def format_problem_statement(problem):
    """Convert raw problem data into a clear business problem statement"""
    title = problem.get('title', '')
    source = problem.get('source', '')
    category = problem.get('category', 'general')
    
    # Extract business opportunity from the problem
    problem_indicators = {
        'technical_problem': 'Technical issue that needs a solution',
        'social_complaint': 'Social media complaint indicating market need',
        'problem_identification': 'Question indicating a problem to solve',
        'general': 'General problem or complaint'
    }
    
    problem_type = problem_indicators.get(category, 'Problem to solve')
    
    # Create a business-focused problem statement
    if 'wedding' in title.lower():
        return f"Wedding Industry Problem: {title}"
    elif 'business' in title.lower() or 'startup' in title.lower():
        return f"Business Problem: {title}"
    elif 'tech' in title.lower() or 'app' in title.lower() or 'software' in title.lower():
        return f"Technology Problem: {title}"
    else:
        return f"General Problem: {title}"

def organize_results_by_source(problems):
    """Organize problems by source with clear sections"""
    organized = {}
    
    for problem in problems:
        source = problem['source'].split('/')[0]  # Get main source name
        if source not in organized:
            organized[source] = []
        organized[source].append(problem)
    
    return organized

def main():
    print("🔍 Problem Finder - Discovering Business Opportunities")
    print("=" * 60)
    
    # Initialize all sources
    sources = [
        RedditSource(subreddits=['weddingplanning', 'AskReddit', 'entrepreneur', 'smallbusiness']),
        GoogleTrendsSource(keywords=['wedding thank you', 'wedding stress', 'business problems', 'startup challenges']),
        QuoraSource(topics=['wedding planning', 'business problems', 'entrepreneurship', 'technology issues']),
        StackOverflowSource(tags=['javascript', 'python', 'react', 'node.js']),
        TwitterSource(keywords=['wedding', 'business', 'startup', 'technology'])
    ]
    
    print("📡 Fetching problems from multiple sources...")
    all_problems = []
    
    for source in sources:
        try:
            problems = source.fetch_problems()
            all_problems.extend(problems)
            print(f"✅ Found {len(problems)} problems from {source.__class__.__name__}")
        except Exception as e:
            print(f"❌ Error with {source.__class__.__name__}: {e}")
    
    # Organize results by source
    organized_problems = organize_results_by_source(all_problems)
    
    # Generate formatted output
    output_lines = []
    output_lines.append("🎯 BUSINESS PROBLEM FINDER RESULTS")
    output_lines.append("=" * 60)
    output_lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output_lines.append(f"Total problems found: {len(all_problems)}")
    output_lines.append("")
    
    # Process each source
    for source_name, problems in organized_problems.items():
        if problems:
            output_lines.append(f"📊 {source_name.upper()} RESULTS ({len(problems)} problems)")
            output_lines.append("-" * 40)
            
            for i, problem in enumerate(problems, 1):
                problem_statement = format_problem_statement(problem)
                output_lines.append(f"{i}. {problem_statement}")
                
                # Add additional context if available
                if 'score' in problem:
                    output_lines.append(f"   📈 Score: {problem['score']}, Answers: {problem.get('answers', 0)}, Views: {problem.get('views', 0)}")
                if 'engagement' in problem:
                    output_lines.append(f"   📈 Engagement: {problem['engagement']} interactions")
                
                output_lines.append(f"   📍 Source: {problem['source']}")
                output_lines.append("")
    
    # Add summary and business opportunities
    output_lines.append("💡 BUSINESS OPPORTUNITY ANALYSIS")
    output_lines.append("=" * 60)
    
    # Count problems by category
    categories = {}
    for problem in all_problems:
        category = problem.get('category', 'general')
        categories[category] = categories.get(category, 0) + 1
    
    output_lines.append("Problem Categories Found:")
    for category, count in categories.items():
        output_lines.append(f"   • {category.replace('_', ' ').title()}: {count} problems")
    
    output_lines.append("")
    output_lines.append("🚀 NEXT STEPS:")
    output_lines.append("1. Review problems in your area of interest")
    output_lines.append("2. Research market size for each problem")
    output_lines.append("3. Validate with potential customers")
    output_lines.append("4. Develop MVP solution")
    output_lines.append("5. Test and iterate")
    
    # Write to file
    output_text = '\n'.join(output_lines)
    output_path = 'problems_output.txt'
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output_text)
    
    print(f"✅ Results written to {output_path}")
    print(f"📊 Found {len(all_problems)} total problems across {len(organized_problems)} sources")
    
    # Auto-open the file (Windows only)
    try:
        os.startfile(output_path)
    except AttributeError:
        print(f"Please open {output_path} manually.")

if __name__ == '__main__':
    main() 