import gradio as gr

# AWS-style architecture diagram HTML
aws_architecture_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sales AI - AWS Architecture</title>
    <style>
        body {
            font-family: 'Amazon Ember', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #10b981 0%, #3b82f6 100%);
            color: #1f2937;
            line-height: 1.4;
        }
        
        .aws-container {
            max-width: 1600px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.15);
            overflow: hidden;
            padding: 30px;
        }
        
        .aws-header {
            background: linear-gradient(135deg, #059669, #2563eb);
            color: white;
            padding: 25px;
            text-align: center;
            border-radius: 15px;
            margin-bottom: 30px;
        }
        
        .aws-header h1 {
            margin: 0;
            font-size: 2.2em;
            font-weight: 600;
        }
        
        .aws-header p {
            margin: 10px 0 0 0;
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .architecture-diagram {
            position: relative;
            background: #f8fafc;
            border: 2px solid #e2e8f0;
            border-radius: 15px;
            padding: 40px;
            margin: 20px 0;
            min-height: 800px;
        }
        
        /* AWS Cloud Container */
        .aws-cloud {
            position: relative;
            border: 3px dashed #059669;
            border-radius: 20px;
            padding: 30px;
            background: rgba(16, 185, 129, 0.02);
            min-height: 700px;
        }
        
        .aws-cloud-label {
            position: absolute;
            top: -15px;
            left: 20px;
            background: white;
            padding: 5px 15px;
            font-weight: bold;
            color: #059669;
            border: 2px solid #059669;
            border-radius: 8px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .aws-logo {
            width: 24px;
            height: 24px;
            background: #ff9900;
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 10px;
        }
        
        /* Client Devices */
        .client-devices {
            position: absolute;
            left: -120px;
            top: 300px;
            border: 2px dashed #6b7280;
            border-radius: 10px;
            padding: 15px;
            background: white;
            text-align: center;
            width: 80px;
        }
        
        .device-icon {
            width: 30px;
            height: 20px;
            background: #4f46e5;
            border-radius: 3px;
            margin: 5px auto;
            position: relative;
        }
        
        .device-icon::after {
            content: '';
            position: absolute;
            bottom: -8px;
            left: 50%;
            transform: translateX(-50%);
            width: 15px;
            height: 3px;
            background: #4f46e5;
            border-radius: 2px;
        }
        
        /* Service Icons */
        .aws-service {
            position: absolute;
            width: 80px;
            height: 80px;
            border-radius: 12px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 11px;
            text-align: center;
            cursor: pointer;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        .aws-service:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 20px rgba(0,0,0,0.25);
        }
        
        .service-number {
            background: white;
            color: #1f2937;
            width: 25px;
            height: 25px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 14px;
            margin-bottom: 5px;
            border: 2px solid #059669;
        }
        
        /* Service Positions */
        .route53 { top: 50px; left: 120px; background: #9d4edd; }
        .cloudfront { top: 50px; left: 220px; background: #9d4edd; }
        .s3-web { top: 50px; left: 320px; background: #059669; }
        .cognito { top: 180px; left: 220px; background: #e74c3c; }
        .lex { top: 300px; left: 120px; background: #059669; }
        .kendra { top: 300px; left: 220px; background: #059669; }
        .s3-docs { top: 150px; left: 450px; background: #059669; }
        .lambda1 { top: 300px; left: 350px; background: #f39c12; }
        .lambda2 { top: 400px; left: 350px; background: #f39c12; }
        .secrets { top: 500px; left: 280px; background: #e74c3c; }
        .salesforce { top: 300px; left: 550px; background: #00a1e0; }
        
        /* Connection Lines */
        .connection {
            position: absolute;
            height: 3px;
            background: #059669;
            z-index: 1;
        }
        
        .connection::after {
            content: '';
            position: absolute;
            right: -8px;
            top: -4px;
            width: 0;
            height: 0;
            border-left: 8px solid #059669;
            border-top: 5px solid transparent;
            border-bottom: 5px solid transparent;
        }
        
        /* Specific connections */
        .conn1 { top: 90px; left: 200px; width: 120px; }
        .conn2 { top: 90px; left: 300px; width: 120px; }
        .conn3 { top: 220px; left: 260px; width: 90px; transform: rotate(45deg); }
        .conn4 { top: 340px; left: 200px; width: 120px; }
        .conn5 { top: 340px; left: 300px; width: 50px; }
        .conn6 { top: 340px; left: 430px; width: 120px; }
        .conn7 { top: 250px; left: 490px; width: 80px; transform: rotate(45deg); }
        .conn8 { top: 440px; left: 430px; width: 120px; }
        
        /* Info Boxes */
        .info-box {
            position: absolute;
            background: white;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            padding: 15px;
            max-width: 200px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            font-size: 12px;
            line-height: 1.4;
        }
        
        .info-box h4 {
            margin: 0 0 8px 0;
            color: #059669;
            font-size: 13px;
        }
        
        .info-box ul {
            margin: 0;
            padding-left: 15px;
        }
        
        .info-s3 { top: 50px; right: 50px; }
        .info-salesforce { bottom: 50px; right: 50px; }
        
        /* Step Flow */
        .step-flow {
            position: absolute;
            bottom: 20px;
            left: 20px;
            right: 20px;
            background: rgba(255,255,255,0.9);
            border-radius: 10px;
            padding: 20px;
            border: 2px solid #e2e8f0;
        }
        
        .step-flow h3 {
            margin: 0 0 15px 0;
            color: #059669;
            text-align: center;
        }
        
        .steps {
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 10px;
        }
        
        .step {
            background: linear-gradient(135deg, #10b981, #3b82f6);
            color: white;
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 11px;
            text-align: center;
            flex: 1;
            min-width: 120px;
        }
        
        /* Legend */
        .legend {
            position: absolute;
            top: 20px;
            right: 20px;
            background: white;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            padding: 15px;
            font-size: 11px;
        }
        
        .legend h4 {
            margin: 0 0 10px 0;
            color: #059669;
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            margin: 5px 0;
            gap: 8px;
        }
        
        .legend-color {
            width: 15px;
            height: 15px;
            border-radius: 3px;
        }
        
        .compute { background: #f39c12; }
        .storage { background: #059669; }
        .ai-ml { background: #059669; }
        .security { background: #e74c3c; }
        .networking { background: #9d4edd; }
        .integration { background: #00a1e0; }
        
        /* Responsive */
        @media (max-width: 1200px) {
            .architecture-diagram {
                transform: scale(0.8);
                transform-origin: top left;
            }
        }
        
        @media (max-width: 900px) {
            .architecture-diagram {
                transform: scale(0.6);
                transform-origin: top left;
                height: 600px;
                overflow: hidden;
            }
        }
    </style>
</head>
<body>
    <div class="aws-container">
        <div class="aws-header">
            <h1>🏗️ Sales AI Assistant - AWS Cloud Architecture</h1>
            <p>Scalable, Secure, and Intelligent Sales Automation Infrastructure</p>
        </div>
        
        <div class="architecture-diagram">
            <!-- Client Devices -->
            <div class="client-devices">
                <div class="device-icon"></div>
                <div class="device-icon"></div>
                <div style="font-size: 10px; margin-top: 8px; font-weight: bold;">Client Devices</div>
            </div>
            
            <!-- AWS Cloud Container -->
            <div class="aws-cloud">
                <div class="aws-cloud-label">
                    <div class="aws-logo">AWS</div>
                    <span>AWS Cloud</span>
                </div>
                
                <!-- AWS Services -->
                <div class="aws-service route53">
                    <div class="service-number">1</div>
                    <div>Route 53</div>
                </div>
                
                <div class="aws-service cloudfront">
                    <div class="service-number">2</div>
                    <div>CloudFront</div>
                </div>
                
                <div class="aws-service s3-web">
                    <div class="service-number">3</div>
                    <div>S3 Web App</div>
                </div>
                
                <div class="aws-service cognito">
                    <div class="service-number">4</div>
                    <div>Cognito Auth</div>
                </div>
                
                <div class="aws-service lex">
                    <div class="service-number">5</div>
                    <div>Amazon Lex</div>
                </div>
                
                <div class="aws-service kendra">
                    <div class="service-number">6</div>
                    <div>Kendra Search</div>
                </div>
                
                <div class="aws-service s3-docs">
                    <div class="service-number">7</div>
                    <div>S3 Documents</div>
                </div>
                
                <div class="aws-service lambda1">
                    <div class="service-number">8</div>
                    <div>Lambda API</div>
                </div>
                
                <div class="aws-service lambda2">
                    <div class="service-number">9</div>
                    <div>Lambda Process</div>
                </div>
                
                <div class="aws-service secrets">
                    <div class="service-number">10</div>
                    <div>Secrets Manager</div>
                </div>
                
                <!-- Connection Lines -->
                <div class="connection conn1"></div>
                <div class="connection conn2"></div>
                <div class="connection conn3"></div>
                <div class="connection conn4"></div>
                <div class="connection conn5"></div>
                <div class="connection conn6"></div>
                <div class="connection conn7"></div>
                <div class="connection conn8"></div>
                
                <!-- Info Boxes -->
                <div class="info-box info-s3">
                    <h4>📄 Document Storage</h4>
                    <ul>
                        <li>Product catalogs</li>
                        <li>Sales guides</li>
                        <li>Training data</li>
                        <li>Customer files</li>
                    </ul>
                </div>
                
                <div class="info-box info-salesforce">
                    <h4>🔗 CRM Integration</h4>
                    <ul>
                        <li>Lead management</li>
                        <li>Customer data</li>
                        <li>Sales pipeline</li>
                        <li>Analytics</li>
                    </ul>
                </div>
                
                <!-- Step Flow -->
                <div class="step-flow">
                    <h3>📋 Data Flow Process</h3>
                    <div class="steps">
                        <div class="step">1. DNS Routing</div>
                        <div class="step">2. CDN Delivery</div>
                        <div class="step">3. User Auth</div>
                        <div class="step">4. AI Chat</div>
                        <div class="step">5. Document Search</div>
                        <div class="step">6. API Processing</div>
                        <div class="step">7. CRM Integration</div>
                        <div class="step">8. Response Generation</div>
                    </div>
                </div>
            </div>
            
            <!-- External Salesforce -->
            <div class="aws-service salesforce">
                <div style="background: white; color: #00a1e0; width: 25px; height: 25px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 14px; margin-bottom: 5px;">SF</div>
                <div>Salesforce CRM</div>
            </div>
            
            <!-- Legend -->
            <div class="legend">
                <h4>🎨 Service Categories</h4>
                <div class="legend-item">
                    <div class="legend-color compute"></div>
                    <span>Compute (Lambda)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color storage"></div>
                    <span>Storage & AI/ML</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color security"></div>
                    <span>Security</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color networking"></div>
                    <span>Networking</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color integration"></div>
                    <span>Integration</span>
                </div>
            </div>
        </div>
        
        <!-- Service Details -->
        <div style="margin-top: 30px; display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
            <div style="background: #f8fafc; border-radius: 10px; padding: 20px; border: 1px solid #e2e8f0;">
                <h3 style="color: #059669; margin-top: 0;">🌐 Frontend & CDN</h3>
                <ul style="margin: 0; padding-left: 20px; line-height: 1.6;">
                    <li><strong>Route 53:</strong> DNS management and health checks</li>
                    <li><strong>CloudFront:</strong> Global content delivery network</li>
                    <li><strong>S3 Web:</strong> Static website hosting (React/Vue app)</li>
                </ul>
            </div>
            
            <div style="background: #f8fafc; border-radius: 10px; padding: 20px; border: 1px solid #e2e8f0;">
                <h3 style="color: #059669; margin-top: 0;">🤖 AI & Intelligence</h3>
                <ul style="margin: 0; padding-left: 20px; line-height: 1.6;">
                    <li><strong>Amazon Lex:</strong> Conversational AI chatbot</li>
                    <li><strong>Kendra:</strong> Intelligent document search</li>
                    <li><strong>Lambda:</strong> Serverless AI processing</li>
                </ul>
            </div>
            
            <div style="background: #f8fafc; border-radius: 10px; padding: 20px; border: 1px solid #e2e8f0;">
                <h3 style="color: #059669; margin-top: 0;">🔐 Security & Auth</h3>
                <ul style="margin: 0; padding-left: 20px; line-height: 1.6;">
                    <li><strong>Cognito:</strong> User authentication and authorization</li>
                    <li><strong>Secrets Manager:</strong> API keys and credentials</li>
                    <li><strong>IAM:</strong> Fine-grained access control</li>
                </ul>
            </div>
        </div>
    </div>
</body>
</html>
"""

# Your original HTML content (keeping the updated HF colors)
original_html_content = """
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
        </div>
    </div>
</body>
</html>
"""

def display_aws_architecture():
    """Function to display AWS-style architecture"""
    return aws_architecture_html

def display_original_architecture():
    """Function to display the original sales architecture"""
    return original_html_content

# Create the Gradio interface
with gr.Blocks(
    title="Sales AI Architecture - AWS Cloud Design",
    theme=gr.themes.Soft(),
    css="""
    .gradio-container {
        max-width: none !important;
        padding: 0 !important;
    }
    """
) as demo:
    
    gr.Markdown("# ☁️ Sales Assistant AI - Cloud Architecture Dashboard")
    gr.Markdown("*Professional AWS-style infrastructure visualization for sales automation*")
    
    with gr.Tab("🏗️ AWS Cloud Architecture"):
        gr.Markdown("""
        ## AWS Infrastructure Design
        
        This tab shows the **AWS cloud infrastructure** that powers the Sales AI Assistant, similar to AWS architecture diagrams you'd see in enterprise documentation.
        
        **Key Features:**
        - ☁️ **Scalable Cloud Infrastructure**: Built on AWS services for enterprise-grade reliability
        - 🔒 **Security-First Design**: Cognito authentication, Secrets Manager, and IAM controls
        - 🤖 **AI-Powered Components**: Amazon Lex for chat, Kendra for intelligent search
        - 🔗 **CRM Integration**: Direct Salesforce connectivity for seamless data flow
        - 📊 **Serverless Processing**: Lambda functions for cost-effective scaling
        """)
        
        aws_output = gr.HTML(
            value=aws_architecture_html,
            label="AWS Cloud Architecture Diagram"
        )
    
    with gr.Tab("📋 Business Process Flow"):
        gr.Markdown("""
        ## Sales Process Architecture
        
        This tab shows the **business process flow** and human-AI collaboration model that defines how the sales system operates.
        
        **Key Highlights:**
        - 👥 **Human-AI Collaboration**: Strategic balance between automation and expertise  
        - 🔄 **Decision Points**: Clear escalation triggers for complex scenarios
        - 📈 **Learning Loop**: Continuous improvement from customer interactions
        - ⚡ **Real-time Processing**: Instant response generation with human oversight
        """)
        
        original_output = gr.HTML(
            value=original_html_content,
            label="Business Process Flow Visualization"
        )
    
    with gr.Tab("🚀 Deployment Guide"):
        gr.Markdown("""
        ## AWS Deployment Instructions
        
        ### Infrastructure as Code (Terraform/CloudFormation)
        
        ```hcl
        # Example Terraform configuration
        resource "aws_s3_bucket" "sales_ai_web" {
          bucket = "sales-ai-web-app"
          
          website {
            index_document = "index.html"
            error_document = "error.html"
          }
        }
        
        resource "aws_cloudfront_distribution" "sales_ai_cdn" {
          origin {
            domain_name = aws_s3_bucket.sales_ai_web.bucket_regional_domain_name
            origin_id   = "S3-sales-ai-web"
          }
          
          enabled             = true
          default_root_object = "index.html"
        }
        
        resource "aws_lex_bot" "sales_assistant" {
          name = "SalesAssistantBot"
          
          intent {
            intent_name = "GetProductInfo"
            sample_utterances = [
              "I need information about products",
              "What products do you have",
              "Show me your catalog"
            ]
          }
        }
        ```
        
        ### Step-by-Step Deployment
        
        #### 1. Frontend Setup (S3 + CloudFront)
        ```bash
        # Create S3 bucket for web hosting
        aws s3 mb s3://your-sales-ai-web-app
        
        # Upload React/Vue app
        aws s3 sync ./dist s3://your-sales-ai-web-app
        
        # Create CloudFront distribution
        aws cloudfront create-distribution --distribution-config file://cloudfront-config.json
        ```
        
        #### 2. AI Services Configuration
        ```bash
        # Create Lex bot
        aws lex-models put-bot --name SalesAssistantBot --cli-input-json file://lex-bot-config.json
        
        # Setup Kendra index
        aws kendra create-index --name SalesDocuments --role-arn arn:aws:iam::account:role/KendraRole
        
        # Upload documents to S3 for Kendra indexing
        aws s3 sync ./documents s3://your-kendra-documents
        ```
        
        #### 3. Lambda Functions
        ```python
        # Example Lambda function for sales processing
        import json
        import boto3
        
        def lambda_handler(event, context):
            # Process customer inquiry
            lex_client = boto3.client('lex-runtime')
            kendra_client = boto3.client('kendra')
            
            # Get user input
            user_input = event['inputTranscript']
            
            # Search knowledge base
            kendra_response = kendra_client.query(
                IndexId='your-kendra-index-id',
                QueryText=user_input
            )
            
            # Generate response
            response = generate_sales_response(kendra_response)
            
            return {
                'statusCode': 200,
                'body': json.dumps(response)
            }
        ```
        
        #### 4. Security Setup
        ```bash
        # Create Cognito User Pool
        aws cognito-idp create-user-pool --pool-name SalesAIUsers
        
        # Store Salesforce credentials in Secrets Manager
        aws secretsmanager create-secret --name salesforce-credentials --secret-string '{"username":"user","password":"pass","token":"token"}'
        
        # Create IAM roles with least privilege
        aws iam create-role --role-name LambdaExecutionRole --assume-role-policy-document file://trust-policy.json
        ```
        
        ### Cost Optimization Tips
        
        - **Use S3 Intelligent Tiering** for document storage
        - **Configure Lambda concurrency limits** to control costs
        - **Implement CloudFront caching** to reduce origin requests
        - **Use Kendra Developer Edition** for smaller deployments
        - **Set up CloudWatch billing alarms** for cost monitoring
        
        ### Monitoring & Logging
        
        ```bash
        # Enable CloudTrail for audit logging
        aws cloudtrail create-trail --name SalesAIAuditTrail --s3-bucket-name audit-logs-bucket
        
        # Create CloudWatch dashboards
        aws cloudwatch put-dashboard --dashboard-name SalesAIDashboard --dashboard-body file://dashboard-config.json
        
        # Set up X-Ray tracing for Lambda functions
        aws lambda update-function-configuration --function-name SalesProcessor --tracing-config Mode=Active
        ```
        """)
    
    with gr.Tab("⚙️ Configuration"):
        gr.Markdown("## System Configuration Options")
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("### AWS Services Configuration")
                
                aws_region = gr.Dropdown(
                    choices=["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"],
                    value="us-east-1",
                    label="AWS Region",
                    info="Primary deployment region"
                )
                
                lex_confidence = gr.Slider(
                    minimum=0.1,
                    maximum=1.0,
                    value=0.8,
                    step=0.1,
                    label="Lex Confidence Threshold",
                    info="Minimum confidence for intent recognition"
                )
                
                kendra_results = gr.Slider(
                    minimum=1,
                    maximum=20,
                    value=5,
                    step=1,
                    label="Kendra Search Results",
                    info="Number of search results to return"
                )
            
            with gr.Column():
                gr.Markdown("### Business Logic Settings")
                
                escalation_threshold = gr.Slider(
                    minimum=1000,
                    maximum=50000,
                    value=10000,
                    step=1000,
                    label="Escalation Threshold ($)",
                    info="Budget threshold for human escalation"
                )
                
                auto_followup = gr.Checkbox(
                    label="Enable Auto Follow-up",
                    value=True,
                    info="Automatically schedule follow-up communications"
                )
                
                sentiment_monitoring = gr.Checkbox(
                    label="Enable Sentiment Analysis",
                    value=True,
                    info="Monitor customer sentiment for escalation triggers"
                )
        
        config_output = gr.JSON(
            label="Current System Configuration",
            value={
                "aws_region": "us-east-1",
                "lex_confidence": 0.8,
                "kendra_results": 5,
                "escalation_threshold": 10000,
                "auto_followup": True,
                "sentiment_monitoring": True,
                "last_updated": "2025-06-17T10:30:00Z"
            }
        )
        
        def update_config(region, lex_conf, kendra_res, threshold, followup, sentiment):
            return {
                "aws_region": region,
                "lex_confidence": lex_conf,
                "kendra_results": kendra_res,
                "escalation_threshold": threshold,
                "auto_followup": followup,
                "sentiment_monitoring": sentiment,
                "deployment_status": "Ready for deployment",
                "estimated_monthly_cost": f"${(threshold/1000 * 50 + kendra_res * 10):.2f}",
                "last_updated": "2025-06-17T10:30:00Z"
            }
        
        # Update configuration when any input changes
        for component in [aws_region, lex_confidence, kendra_results, escalation_threshold, auto_followup, sentiment_monitoring]:
            component.change(
                fn=update_config,
                inputs=[aws_region, lex_confidence, kendra_results, escalation_threshold, auto_followup, sentiment_monitoring],
                outputs=config_output
            )
    
    with gr.Tab("📊 Cost Calculator"):
        gr.Markdown("## AWS Cost Estimation")
        
        with gr.Row():
            with gr.Column():
                monthly_users = gr.Slider(
                    minimum=100,
                    maximum=100000,
                    value=5000,
                    step=100,
                    label="Monthly Active Users",
                    info="Expected number of users per month"
                )
                
                conversations_per_user = gr.Slider(
                    minimum=1,
                    maximum=50,
                    value=10,
                    step=1,
                    label="Conversations per User",
                    info="Average conversations per user per month"
                )
                
                document_storage_gb = gr.Slider(
                    minimum=1,
                    maximum=1000,
                    value=100,
                    step=10,
                    label="Document Storage (GB)",
                    info="Total storage needed for documents"
                )
            
            with gr.Column():
                def calculate_costs(users, conversations, storage):
                    # AWS pricing estimates (simplified)
                    lex_cost = (users * conversations * 0.004)  # $0.004 per request
                    kendra_cost = 810  # Base monthly cost for Kendra
                    s3_cost = storage * 0.023  # $0.023 per GB per month
                    lambda_cost = (users * conversations * 0.0000002)  # Very cheap
                    cloudfront_cost = (users * 0.01)  # CDN costs
                    
                    total_cost = lex_cost + kendra_cost + s3_cost + lambda_cost + cloudfront_cost
                    
                    return {
                        "Amazon Lex": f"${lex_cost:.2f}",
                        "Amazon Kendra": f"${kendra_cost:.2f}",
                        "S3 Storage": f"${s3_cost:.2f}",
                        "Lambda Functions": f"${lambda_cost:.2f}",
                        "CloudFront CDN": f"${cloudfront_cost:.2f}",
                        "Total Monthly Cost": f"${total_cost:.2f}",
                        "Cost per User": f"${total_cost/users:.4f}"
                    }
                
                cost_breakdown = gr.JSON(
                    label="Monthly Cost Breakdown",
                    value=calculate_costs(5000, 10, 100)
                )
                
                # Update costs when sliders change
                for slider in [monthly_users, conversations_per_user, document_storage_gb]:
                    slider.change(
                        fn=calculate_costs,
                        inputs=[monthly_users, conversations_per_user, document_storage_gb],
                        outputs=cost_breakdown
                    )
        
        gr.Markdown("""
        ### 💡 Cost Optimization Recommendations
        
        - **Start with Kendra Developer Edition** ($810/month) for up to 5 users
        - **Use S3 Intelligent Tiering** to automatically move old documents to cheaper storage
        - **Implement Lambda Provisioned Concurrency** only for high-traffic functions  
        - **Cache frequently accessed data** in CloudFront to reduce backend calls
        - **Monitor usage with CloudWatch** and set up billing alerts
        - **Consider Reserved Instances** for predictable workloads after 6 months
        """)

# Launch the app
if __name__ == "__main__":
    demo.launch(
        share=True,
        server_name="0.0.0.0",
        server_port=7862
    )
