import gradio as gr

# Your HTML content as a string
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sales Assistant AI Architecture</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #10b981 0%, #3b82f6 100%);
            color: #1f2937;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.15);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #059669, #2563eb);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }
        
        .content {
            padding: 40px;
        }
        
        .architecture-flow {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-bottom: 50px;
        }
        
        .stage {
            background: #f9fafb;
            border-radius: 15px;
            padding: 25px;
            border-left: 5px solid #059669;
            position: relative;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .stage:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .stage-header {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .stage-number {
            background: #059669;
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 15px;
        }
        
        .stage-title {
            font-size: 1.3em;
            font-weight: 600;
            color: #111827;
        }
        
        .ai-tag, .human-tag, .hybrid-tag {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: 600;
            margin: 5px 5px 5px 0;
        }
        
        .ai-tag {
            background: #d1fae5;
            color: #065f46;
            border: 1px solid #059669;
        }
        
        .human-tag {
            background: #dbeafe;
            color: #1e40af;
            border: 1px solid #2563eb;
        }
        
        .hybrid-tag {
            background: #e0e7ff;
            color: #3730a3;
            border: 1px solid #4f46e5;
        }
        
        .decision-points {
            background: #fef2f2;
            border-radius: 15px;
            padding: 25px;
            margin: 30px 0;
            border-left: 5px solid #dc2626;
        }
        
        .sequence-diagram {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-top: 20px;
            overflow-x: auto;
            min-width: 900px;
        }
        
        .actors-container {
            display: flex;
            justify-content: space-between;
            margin-bottom: 30px;
            position: relative;
        }
        
        .actor {
            background: #059669;
            color: white;
            padding: 12px 16px;
            border-radius: 8px;
            font-weight: 600;
            text-align: center;
            min-width: 100px;
            font-size: 0.9em;
            box-shadow: 0 4px 12px rgba(5, 150, 105, 0.3);
            flex: 1;
            margin: 0 10px;
            max-width: 140px;
        }
        
        .sequence-content {
            position: relative;
            min-height: 900px;
        }
        
        .lifelines-container {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 100%;
            display: flex;
            justify-content: space-between;
            padding: 0 70px;
        }
        
        .lifeline {
            width: 2px;
            height: 100%;
            background: #9ca3af;
            position: relative;
        }
        
        .lifeline::before {
            content: '';
            position: absolute;
            top: -5px;
            left: -4px;
            width: 10px;
            height: 10px;
            background: #059669;
            border-radius: 50%;
        }
        
        .interactions-container {
            position: relative;
            padding: 20px 0;
        }
        
        .sequence-step {
            position: absolute;
            width: 100%;
            height: 40px;
            display: flex;
            align-items: center;
        }
        
        .arrow-line {
            position: absolute;
            height: 2px;
            background: #111827;
            z-index: 2;
        }
        
        .arrow-line.conditional {
            background: #d97706;
            border-top: 2px dashed #d97706;
            background: none;
        }
        
        .arrow-line[data-from="0"][data-to="1"] { left: 70px; width: calc(20% - 20px); }
        .arrow-line[data-from="1"][data-to="0"] { left: 70px; width: calc(20% - 20px); }
        .arrow-line[data-from="1"][data-to="2"] { left: calc(20% + 50px); width: calc(20% - 20px); }
        .arrow-line[data-from="2"][data-to="1"] { left: calc(20% + 50px); width: calc(20% - 20px); }
        .arrow-line[data-from="1"][data-to="3"] { left: calc(20% + 50px); width: calc(40% - 20px); }
        .arrow-line[data-from="3"][data-to="0"] { left: 70px; width: calc(60% - 20px); }
        .arrow-line[data-from="3"][data-to="4"] { left: calc(60% + 50px); width: calc(20% - 20px); }
        .arrow-line[data-from="4"][data-to="3"] { left: calc(60% + 50px); width: calc(20% - 20px); }
        .arrow-line[data-from="3"][data-to="5"] { left: calc(60% + 50px); width: calc(40% - 20px); }
        .arrow-line[data-from="5"][data-to="3"] { left: calc(60% + 50px); width: calc(40% - 20px); }
        
        .arrow-head {
            position: absolute;
            width: 0;
            height: 0;
            top: -4px;
        }
        
        .arrow-head.right {
            right: -8px;
            border-left: 8px solid #111827;
            border-top: 4px solid transparent;
            border-bottom: 4px solid transparent;
        }
        
        .arrow-head.left {
            left: -8px;
            border-right: 8px solid #111827;
            border-top: 4px solid transparent;
            border-bottom: 4px solid transparent;
        }
        
        .conditional .arrow-head.right {
            border-left-color: #d97706;
        }
        
        .conditional .arrow-head.left {
            border-right-color: #d97706;
        }
        
        .message-box {
            background: #f3f4f6;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 0.85em;
            font-weight: 500;
            color: #111827;
            white-space: nowrap;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            position: absolute;
            z-index: 3;
        }
        
        .message-box[data-position="center"] {
            left: 50%;
            transform: translateX(-50%);
            top: -30px;
        }
        
        .message-box[data-position="right"] {
            right: 20px;
            top: -30px;
        }
        
        .message-box.conditional {
            background: #fef3c7;
            border-left: 3px solid #d97706;
        }
        
        .message-box.human-enhanced {
            background: #d1fae5;
            border-left: 3px solid #059669;
            border: 2px solid #059669;
        }
        
        .message-box.manager-approved {
            background: #e0e7ff;
            border-left: 3px solid #4f46e5;
            border: 2px solid #4f46e5;
            font-weight: 600;
        }
        
        .message-box.self-message {
            background: #d1fae5;
            border-left: 3px solid #059669;
        }
        
        .decision-step {
            height: 60px;
            justify-content: center;
        }
        
        .decision-box-new {
            background: #fef2f2;
            border: 2px solid #dc2626;
            border-radius: 10px;
            padding: 15px 20px;
            text-align: center;
            font-size: 0.9em;
            box-shadow: 0 4px 12px rgba(220, 38, 38, 0.2);
            max-width: 450px;
            margin: 0 auto;
        }
        
        .conditional-step {
            opacity: 0.8;
        }
        
        .self-arrow {
            position: absolute;
            width: 30px;
            height: 30px;
            border: 2px solid #059669;
            border-radius: 50%;
            background: white;
        }
        
        .self-arrow[data-actor="1"] {
            left: calc(20% + 50px);
        }
        
        .legend-sequence {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #e5e7eb;
            flex-wrap: wrap;
        }
        
        .legend-item-seq {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 0.9em;
        }
        
        .arrow-sample {
            width: 30px;
            height: 2px;
            background: #111827;
            position: relative;
        }
        
        .arrow-sample .arrow-head.right {
            right: -6px;
            top: -3px;
            border-left: 6px solid #111827;
            border-top: 3px solid transparent;
            border-bottom: 3px solid transparent;
        }
        
        .arrow-sample .arrow-head.left {
            left: -6px;
            top: -3px;
            border-right: 6px solid #111827;
            border-top: 3px solid transparent;
            border-bottom: 3px solid transparent;
        }
        
        .arrow-sample.conditional {
            background: none;
            border-top: 2px dashed #d97706;
        }
        
        .decision-sample {
            width: 20px;
            height: 20px;
            background: #fef2f2;
            border: 2px solid #dc2626;
            border-radius: 4px;
        }
        
        .human-enhanced-sample {
            width: 30px;
            height: 15px;
            background: #d1fae5;
            border: 2px solid #059669;
            border-radius: 4px;
        }
        
        .manager-approved-sample {
            width: 30px;
            height: 15px;
            background: #e0e7ff;
            border: 2px solid #4f46e5;
            border-radius: 4px;
        }
        
        .enhancement-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            margin-top: 30px;
        }
        
        .enhancement-card {
            background: linear-gradient(135deg, #10b981, #3b82f6);
            color: white;
            border-radius: 15px;
            padding: 25px;
            transition: transform 0.3s ease;
        }
        
        .enhancement-card:hover {
            transform: scale(1.05);
        }
        
        .enhancement-title {
            font-size: 1.2em;
            font-weight: 600;
            margin-bottom: 15px;
        }
        
        .enhancement-items {
            list-style: none;
            padding: 0;
        }
        
        .enhancement-items li {
            padding: 5px 0;
            padding-left: 20px;
            position: relative;
        }
        
        .enhancement-items li:before {
            content: "→";
            position: absolute;
            left: 0;
            color: #a7f3d0;
        }
        
        .flow-arrow {
            text-align: center;
            font-size: 2em;
            color: #059669;
            margin: 20px 0;
        }
        
        .section-title {
            font-size: 2em;
            color: #111827;
            margin: 40px 0 20px 0;
            text-align: center;
            position: relative;
        }
        
        .section-title:after {
            content: "";
            display: block;
            width: 80px;
            height: 3px;
            background: #059669;
            margin: 10px auto;
        }
        
        .legend {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin: 30px 0;
            flex-wrap: wrap;
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        @media (max-width: 768px) {
            .architecture-flow {
                grid-template-columns: 1fr;
            }
            
            .legend {
                flex-direction: column;
                align-items: center;
                gap: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Sales Assistant AI Architecture</h1>
            <p>Human-AI Intelligence Management Framework</p>
        </div>
        
        <div class="content">
            <div class="legend">
                <div class="legend-item">
                    <span class="ai-tag">AI Chatbot</span>
                    <span>Machine handles dialogue with customer</span>
                </div>
                <div class="legend-item">
                    <span class="human-tag">Human Staff</span>
                    <span>Human makes key decisions & learn new tactics from performance</span>
                </div>
                <div class="legend-item">
                    <span class="hybrid-tag">Hybrid</span>
                    <span>AI + Human collaboration continuously</span>
                </div>
            </div>

            <h2 class="section-title">System Architecture Flow</h2>
            
            <div class="architecture-flow">
                <div class="stage">
                    <div class="stage-header">
                        <div class="stage-number">1</div>
                        <div class="stage-title">Data Collection Layer</div>
                    </div>
                    <div class="ai-tag">AI Agent</div>
                    <p><strong>Web Scraping Engine:</strong> Automated product data extraction, image URL collection, price monitoring, bulk purchase discount</p>
                    <p><strong>Data Processing:</strong> AI database creation, product categorization, content normalization</p>
                    <p><strong>Human Job:</strong> Configure scraping rules in changing configuration, validate data quality, manage compliance</p>
                </div>

                <div class="stage">
                    <div class="stage-header">
                        <div class="stage-number">2</div>
                        <div class="stage-title">Customer Engagement</div>
                    </div>
                    <div class="hybrid-tag">Hybrid</div>
                    <p><strong>AI Chatbot:</strong> Initial conversation, basic qualification, FAQ handling, prompt engineering for data collection</p>
                    <p><strong>Human Monitoring:</strong> Real-time conversation oversight, intervention triggers, quality control</p>
                    <p><strong>Escalation Points:</strong> Complex queries, high-value prospects, emotional situations</p>
                </div>

                <div class="stage">
                    <div class="stage-header">
                        <div class="stage-number">3</div>
                        <div class="stage-title">Lead Qualification</div>
                    </div>
                    <div class="ai-tag">AI Agent</div>
                    <p><strong>Intent Analysis:</strong> Purchase probability scoring, budget assessment, timeline evaluation</p>
                    <p><strong>Data Extraction:</strong> Name, email, requirements, budget collection through conversational AI</p>
                    <p><strong>Lead Scoring:</strong> Automated priority ranking based on multiple factors</p>
                </div>

                <div class="stage">
                    <div class="stage-header">
                        <div class="stage-number">4</div>
                        <div class="stage-title">Quotation Interplay</div>
                    </div>
                    <div class="hybrid-tag">Hybrid</div>
                    <p><strong>AI Matching:</strong> Customer needs vs inventory analysis, initial price suggestions</p>
                    <p><strong>Human Decision:</strong> Final pricing strategy, business tactics application, negotiation parameters</p>
                    <p><strong>Approval Workflow:</strong> Tiered authorization based on deal size and complexity</p>
                </div>

                <div class="stage">
                    <div class="stage-header">
                        <div class="stage-number">5</div>
                        <div class="stage-title">Response Generation</div>
                    </div>
                    <div class="hybrid-tag">Hybrid</div>
                    <p><strong>AI Content Creation:</strong> Email/message generation with selected tone, product recommendations</p>
                    <p><strong>Human Review:</strong> Content approval, relationship considerations, custom modifications</p>
                    <p><strong>Multi-channel Delivery:</strong> Email, SMS, WhatsApp, or other preferred channels</p>
                </div>

                <div class="stage">
                    <div class="stage-header">
                        <div class="stage-number">6</div>
                        <div class="stage-title">Follow-up & Analytics</div>
                    </div>
                    <div class="ai-tag">AI Data Scientist Agent</div>
                    <p><strong>Automated Follow-up:</strong> Scheduled touchpoints, engagement tracking</p>
                    <p><strong>Performance Analytics:</strong> Conversion tracking, ROI analysis, system optimization</p>
                    <p><strong>Learning Loop:</strong> Continuous improvement from outcomes</p>
                </div>
            </div>

            <div class="decision-points">
                <h2 class="section-title">System Sequence Diagram</h2>
                
                <div class="sequence-diagram">
                    <div class="actors-container">
                        <div class="actor" data-position="0">Customer</div>
                        <div class="actor" data-position="1">AI Chatbot</div>
                        <div class="actor" data-position="2">Embedded Database</div>
                        <div class="actor" data-position="3">Human Agent</div>
                        <div class="actor" data-position="4">Quotation Interplay</div>
                        <div class="actor" data-position="5">AI Email Generator</div>
                    </div>
                    
                    <div class="sequence-content">
                        <div class="lifelines-container">
                            <div class="lifeline" data-actor="0"></div>
                            <div class="lifeline" data-actor="1"></div>
                            <div class="lifeline" data-actor="2"></div>
                            <div class="lifeline" data-actor="3"></div>
                            <div class="lifeline" data-actor="4"></div>
                            <div class="lifeline" data-actor="5"></div>
                        </div>
                        
                        <div class="interactions-container">
                            <div class="sequence-step" style="top: 20px;">
                                <div class="arrow-line" data-from="0" data-to="1">
                                    <div class="arrow-head right"></div>
                                </div>
                                <div class="message-box" data-position="center">1. Initial inquiry</div>
                            </div>
                            
                            <div class="sequence-step" style="top: 70px;">
                                <div class="arrow-line" data-from="1" data-to="2">
                                    <div class="arrow-head right"></div>
                                </div>
                                <div class="message-box" data-position="center">2. Query product data</div>
                            </div>
                            
                            <div class="sequence-step" style="top: 125px;">
                                <div class="arrow-line" data-from="2" data-to="1">
                                    <div class="arrow-head left"></div>
                                </div>
                                <div class="message-box human-enhanced" data-position="center">3. Return product info (Backend: Human + AI scraper interplay)</div>
                            </div>
                            
                            <div class="sequence-step" style="top: 180px;">
                                <div class="arrow-line" data-from="1" data-to="0">
                                    <div class="arrow-head left"></div>
                                </div>
                                <div class="message-box human-enhanced" data-position="center">4. Present options + qualify (Backend: Human experience + prompt engineering )</div>
                            </div>
                            
                            <div class="sequence-step" style="top: 235px;">
                                <div class="arrow-line" data-from="0" data-to="1">
                                    <div class="arrow-head right"></div>
                                </div>
                                <div class="message-box" data-position="center">5. Seek customer details (name, email, budget by AI engagement with prompt engineering)</div>
                            </div>
                            
                            <div class="sequence-step decision-step" style="top: 270px;">
                                <div class="decision-box-new">
                                    <strong>Decision Point:</strong><br>
                                    Budget > $10K OR Complex query OR Negative sentiment?
                                </div>
                            </div>
                            
                            <div class="sequence-step conditional-step" style="top: 375px;">
                                <div class="arrow-line conditional" data-from="1" data-to="3">
                                    <div class="arrow-head right"></div>
                                </div>
                                <div class="message-box conditional" data-position="center">6. IF escalation: Alert human staff</div>
                            </div>
                            
                            <div class="sequence-step conditional-step" style="top: 430px;">
                                <div class="arrow-line conditional" data-from="3" data-to="0">
                                    <div class="arrow-head left"></div>
                                </div>
                                <div class="message-box conditional" data-position="center">7. Take over conversation</div>
                            </div>
                            
                            <div class="sequence-step" style="top: 495px;">
                                <div class="arrow-line" data-from="3" data-to="4">
                                    <div class="arrow-head right"></div>
                                </div>
                                <div class="message-box" data-position="center">8. Generate quote request</div>
                            </div>
                            
                            <div class="sequence-step decision-step" style="top: 527px;">
                                <div class="decision-box-new">
                                    <strong>Human Decision:</strong><br>
                                    Pricing strategy, Business tactics, Inventory allocation
                                </div>
                            </div>
                            
                            <div class="sequence-step" style="top: 630px;">
                                <div class="arrow-line" data-from="4" data-to="3">
                                    <div class="arrow-head left"></div>
                                </div>
                                <div class="message-box manager-approved" data-position="center">9. Approved quote + tone (Manager/Supervisor approval)</div>
                            </div>
                            
                            <div class="sequence-step" style="top: 685px;">
                                <div class="arrow-line" data-from="3" data-to="5">
                                    <div class="arrow-head right"></div>
                                </div>
                                <div class="message-box" data-position="center">10. LLM Generate response</div>
                            </div>
                            
                            <div class="sequence-step" style="top: 740px;">
                                <div class="arrow-line" data-from="3" data-to="0">
                                    <div class="arrow-head left"></div>
                                </div>
                                <div class="message-box" data-position="center">11. Human Oversight then Send final proposal</div>
                            </div>
                            
                            <div class="sequence-step" style="top: 800px;">
                                <div class="arrow-line" data-from="0" data-to="1">
                                    <div class="arrow-head right"></div>
                                </div>
                                <div class="message-box" data-position="center">12. Response/Feedback</div>
                            </div>
                            
                            <div class="sequence-step" style="top: 830px;">
                                <div class="self-arrow" data-actor="1"></div>
                                <div class="message-box self-message" data-position="right">13. Learn from outcome</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="legend-sequence">
                        <div class="legend-item-seq">
                            <div class="arrow-sample">
                                <div class="arrow-head right"></div>
                            </div>
                            <span>Request/Command</span>
                        </div>
                        <div class="legend-item-seq">
                            <div class="arrow-sample">
                                <div class="arrow-head left"></div>
                            </div>
                            <span>Response/Data</span>
                        </div>
                        <div class="legend-item-seq">
                            <div class="arrow-sample conditional"></div>
                            <span>Conditional Flow</span>
                        </div>
                        <div class="legend-item-seq">
                            <div class="decision-sample"></div>
                            <span>Decision Point</span>
                        </div>
                        <div class="legend-item-seq">
                            <div class="human-enhanced-sample"></div>
                            <span>Human-AI Collaboration</span>
                        </div>
                        <div class="legend-item-seq">
                            <div class="manager-approved-sample"></div>
                            <span>Manager Approval</span>
                        </div>
                    </div>
                </div>
            </div>

            <h2 class="section-title">Enhancement Opportunities</h2>
            
            <div class="enhancement-grid">
                <div class="enhancement-card">
                    <div class="enhancement-title">🧠 AI Intelligence Amplifiers</div>
                    <ul class="enhancement-items">
                        <li>Customer journey mapping</li>
                        <li>Behavioral pattern recognition</li>
                        <li>Revenue attribution modeling</li>
                        <li>Market trend analysis</li>
                        <li>Competitive intelligence</li>
                    </ul>
                </div>
                
                <div class="enhancement-card">
                    <div class="enhancement-title">🛡️ Quality & Compliance</div>
                    <ul class="enhancement-items">
                        <li>Automated conversation auditing</li>
                        <li>Brand voice consistency checks</li>
                        <li>Legal compliance monitoring</li>
                        <li>Data privacy protection</li>
                        <li>Error detection & prevention</li>
                    </ul>
                </div>
                
                <div class="enhancement-card">
                    <div class="enhancement-title">🚀 Scalability Features</div>
                    <ul class="enhancement-items">
                        <li>Multi-tenant architecture</li>
                        <li>API integration framework</li>
                        <li>White-label customization</li>
                        <li>Industry-specific modules</li>
                        <li>Global deployment support</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

def display_architecture():
    """Function to display the sales AI architecture"""
    return html_content

# Create the Gradio interface
with gr.Blocks(
    title="Sales Assistant AI Architecture",
    theme=gr.themes.Soft(),
    css="""
    .gradio-container {
        max-width: none !important;
        padding: 0 !important;
    }
    """
) as demo:
    
    gr.Markdown("# 🤖 Sales Assistant AI Architecture Dashboard")
    gr.Markdown("*Interactive visualization of Human-AI Intelligence Management Framework*")
    
    with gr.Tab("📊 Architecture Overview"):
        html_output = gr.HTML(
            value=html_content,
            label="Sales AI Architecture Visualization"
        )
    
    with gr.Tab("📋 Implementation Guide"):
        gr.Markdown("""
        ## 🚀 How to Deploy This Architecture
        
        ### Prerequisites
        - Python environment with required AI/ML libraries
        - Database setup (PostgreSQL/MongoDB recommended)
        - API integrations for communication channels
        - Human oversight dashboard
        
        ### Key Components to Implement
        
        **1. Data Collection Layer**
        - Web scraping infrastructure
        - Data validation pipelines
        - Compliance monitoring
        
        **2. AI Chatbot Engine**
        - Natural language processing
        - Intent recognition
        - Conversation flow management
        
        **3. Human-AI Interface**
        - Real-time monitoring dashboard
        - Escalation triggers
        - Approval workflows
        
        **4. Analytics & Learning**
        - Performance tracking
        - Outcome analysis
        - Continuous improvement loops
        
        ### Technology Stack Recommendations
        - **Backend**: Python/FastAPI or Node.js
        - **AI/ML**: OpenAI GPT, Hugging Face Transformers
        - **Database**: PostgreSQL + Vector DB (Pinecone/Weaviate)
        - **Frontend**: React/Vue.js for dashboards
        - **Monitoring**: Prometheus + Grafana
        - **Communication**: Twilio, SendGrid APIs
        """)
    
    with gr.Tab("⚙️ Configuration"):
        gr.Markdown("## System Configuration Options")
        
        with gr.Row():
            with gr.Column():
                escalation_threshold = gr.Slider(
                    minimum=1000,
                    maximum=50000,
                    value=10000,
                    step=1000,
                    label="Escalation Threshold ($)",
                    info="Budget threshold for human escalation"
                )
                
                response_time = gr.Slider(
                    minimum=1,
                    maximum=60,
                    value=5,
                    step=1,
                    label="Max AI Response Time (seconds)",
                    info="Maximum time for AI to generate response"
                )
            
            with gr.Column():
                human_override = gr.Checkbox(
                    label="Enable Human Override",
                    value=True,
                    info="Allow humans to take over conversations"
                )
                
                sentiment_monitoring = gr.Checkbox(
                    label="Enable Sentiment Monitoring",
                    value=True,
                    info="Monitor customer sentiment for escalation"
                )
        
        config_output = gr.JSON(
            label="Current Configuration",
            value={
                "escalation_threshold": 10000,
                "response_time": 5,
                "human_override": True,
                "sentiment_monitoring": True
            }
        )
        
        def update_config(threshold, time, override, sentiment):
            return {
                "escalation_threshold": threshold,
                "response_time": time,
                "human_override": override,
                "sentiment_monitoring": sentiment,
                "last_updated": "2025-06-16T10:30:00Z"
            }
        
        for component in [escalation_threshold, response_time, human_override, sentiment_monitoring]:
            component.change(
                fn=update_config,
                inputs=[escalation_threshold, response_time, human_override, sentiment_monitoring],
                outputs=config_output
            )

# Launch the app
if __name__ == "__main__":
    demo.launch(
        share=True,
        server_name="0.0.0.0",
        server_port=7860
    )
