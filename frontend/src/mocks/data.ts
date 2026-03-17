export const MOCK_DOCUMENTS = [
  {
    document_id: 1,
    user_id: 1,
    title: 'Artificial_Neural_Network_Model_for_Prediction_of_Drilling_Rate.pdf',
    file_path: '/data/Artificial_Neural_Network_Model_for_Prediction_of_Drilling_Rate.pdf',
    page_count: 12,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    tags: ['Engineering', 'ANN'],
    status: 'processed'
  },
  {
    document_id: 2,
    user_id: 1,
    title: '2206.01062.pdf',
    file_path: '/data/2206.01062.pdf',
    page_count: 28,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    tags: ['AI', 'Research'],
    status: 'processed'
  },
  {
    document_id: 3,
    user_id: 1,
    title: '2203.01017v2.pdf',
    file_path: '/data/2203.01017v2.pdf',
    page_count: 45,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    tags: ['Deep Learning', 'Vision'],
    status: 'processed'
  }
];

export const MOCK_CHAT_RESPONSES: Record<string, string> = {
  default: `Based on your documents, here's what I found:

The research paper presents a novel approach to neural network applications in drilling rate prediction. The methodology combines traditional machine learning techniques with deep learning architectures to achieve more accurate predictions.

Key findings include:
• 15% improvement in prediction accuracy compared to baseline models
• The proposed ANN model handles variable drilling conditions effectively
• Real-time adaptation capabilities show promising results

Would you like me to elaborate on any specific aspect of these findings?`,
  
  summarize: `This document appears to be a technical research paper focused on Artificial Neural Network (ANN) models for predicting drilling rates in oil and gas operations.

The paper covers:
• Methodology for neural network design
• Data collection and preprocessing
• Model training and validation results
• Performance comparisons with traditional methods

The authors conclude that ANN-based approaches offer significant advantages in handling the complex, non-linear relationships inherent in drilling operations.`,

  methodology: `The methodology section details:

1. **Data Collection**: Historical drilling data from multiple wells
2. **Feature Engineering**: 12 input parameters including rock properties, drilling parameters
3. **Model Architecture**: Feedforward neural network with 3 hidden layers
4. **Training**: Backpropagation with adaptive learning rate
5. **Validation**: Cross-validation with 5 folds

The approach demonstrates robust performance across different drilling scenarios.`,

  findings: `Key findings from the research:

• Prediction accuracy improved by 15% over conventional models
• Model generalizes well across different geological formations
• Computational efficiency allows real-time predictions
• Feature importance analysis reveals drilling speed and bit type as most influential factors

The results support the hypothesis that neural networks can effectively model the complex relationships in drilling operations.`
};

export function getMockChatResponse(userMessage: string): string {
  const lower = userMessage.toLowerCase();
  
  if (lower.includes('summarize')) return MOCK_CHAT_RESPONSES.summarize;
  if (lower.includes('methodolog')) return MOCK_CHAT_RESPONSES.methodology;
  if (lower.includes('finding') || lower.includes('result')) return MOCK_CHAT_RESPONSES.findings;
  
  return MOCK_CHAT_RESPONSES.default;
}

export const MOCK_USER = {
  user_id: 1,
  email: 'dev@noetix.ai',
  username: 'DevUser',
  role: 'user',
  is_active: true,
  is_superuser: false,
  full_name: 'Development User'
};
