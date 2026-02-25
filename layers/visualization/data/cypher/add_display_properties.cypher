// Display Properties Migration
// Auto-generated styling for UK Curriculum Knowledge Graph
// Color scheme: Tailwind CSS palette
// Icons: Material Design icon names

// Curriculum - Structure
MATCH (n:Curriculum)
SET n.display_color = '#1F2937',
    n.display_icon = 'account_balance',
    n.display_category = 'Structure';

// KeyStage - Structure
MATCH (n:KeyStage)
SET n.display_color = '#374151',
    n.display_icon = 'stairs',
    n.display_category = 'Structure';

// Year - Structure
MATCH (n:Year)
SET n.display_color = '#4B5563',
    n.display_icon = 'event',
    n.display_category = 'Structure';

// Subject - UK Curriculum
MATCH (n:Subject)
SET n.display_color = '#DC2626',
    n.display_icon = 'menu_book',
    n.display_category = 'UK Curriculum';

// Programme - UK Curriculum
MATCH (n:Programme)
SET n.display_color = '#1E3A8A',
    n.display_icon = 'assignment',
    n.display_category = 'UK Curriculum';

// Domain - UK Curriculum
MATCH (n:Domain)
SET n.display_color = '#8B5CF6',
    n.display_icon = 'folder',
    n.display_category = 'UK Curriculum';

// Objective - UK Curriculum
MATCH (n:Objective)
SET n.display_color = '#10B981',
    n.display_icon = 'flag',
    n.display_category = 'UK Curriculum';

// Concept - UK Curriculum
MATCH (n:Concept)
SET n.display_color = '#3B82F6',
    n.display_icon = 'lightbulb_outline',
    n.display_category = 'UK Curriculum';

// ConceptCluster - UK Curriculum
MATCH (n:ConceptCluster)
SET n.display_color = '#6366F1',
    n.display_icon = 'view_module',
    n.display_category = 'UK Curriculum';

// SourceDocument - Structure
MATCH (n:SourceDocument)
SET n.display_color = '#6B7280',
    n.display_icon = 'description',
    n.display_category = 'Structure';

// WorkingScientifically - Epistemic Skills
MATCH (n:WorkingScientifically)
SET n.display_color = '#14B8A6',
    n.display_icon = 'science',
    n.display_category = 'Epistemic Skills';

// ReadingSkill - Epistemic Skills
MATCH (n:ReadingSkill)
SET n.display_color = '#EC4899',
    n.display_icon = 'menu_book',
    n.display_category = 'Epistemic Skills';

// MathematicalReasoning - Epistemic Skills
MATCH (n:MathematicalReasoning)
SET n.display_color = '#F59E0B',
    n.display_icon = 'calculate',
    n.display_category = 'Epistemic Skills';

// GeographicalSkill - Epistemic Skills
MATCH (n:GeographicalSkill)
SET n.display_color = '#059669',
    n.display_icon = 'public',
    n.display_category = 'Epistemic Skills';

// HistoricalThinking - Epistemic Skills
MATCH (n:HistoricalThinking)
SET n.display_color = '#92400E',
    n.display_icon = 'history_edu',
    n.display_category = 'Epistemic Skills';

// ComputationalThinking - Epistemic Skills
MATCH (n:ComputationalThinking)
SET n.display_color = '#4F46E5',
    n.display_icon = 'computer',
    n.display_category = 'Epistemic Skills';

// TestFramework - Assessment
MATCH (n:TestFramework)
SET n.display_color = '#374151',
    n.display_icon = 'quiz',
    n.display_category = 'Assessment';

// TestPaper - Assessment
MATCH (n:TestPaper)
SET n.display_color = '#4B5563',
    n.display_icon = 'description',
    n.display_category = 'Assessment';

// ContentDomainCode - Assessment
MATCH (n:ContentDomainCode)
SET n.display_color = '#6B7280',
    n.display_icon = 'bookmark',
    n.display_category = 'Assessment';

// Framework - CASE Standards
MATCH (n:Framework)
SET n.display_color = '#EA580C',
    n.display_icon = 'account_balance',
    n.display_category = 'CASE Standards';

// Dimension - CASE Standards
MATCH (n:Dimension)
SET n.display_color = '#C2410C',
    n.display_icon = 'view_in_ar',
    n.display_category = 'CASE Standards';

// CoreIdea - CASE Standards
MATCH (n:CoreIdea)
SET n.display_color = '#B45309',
    n.display_icon = 'school',
    n.display_category = 'CASE Standards';

// CrosscuttingConcept - CASE Standards
MATCH (n:CrosscuttingConcept)
SET n.display_color = '#15803D',
    n.display_icon = 'hub',
    n.display_category = 'CASE Standards';

// Practice - CASE Standards
MATCH (n:Practice)
SET n.display_color = '#0284C7',
    n.display_icon = 'engineering',
    n.display_category = 'CASE Standards';

// PerformanceExpectation - CASE Standards
MATCH (n:PerformanceExpectation)
SET n.display_color = '#6B7280',
    n.display_icon = 'assessment',
    n.display_category = 'CASE Standards';

// GradeBand - CASE Standards
MATCH (n:GradeBand)
SET n.display_color = '#9CA3AF',
    n.display_icon = 'grade',
    n.display_category = 'CASE Standards';

// MathPractice - CASE Standards
MATCH (n:MathPractice)
SET n.display_color = '#D97706',
    n.display_icon = 'functions',
    n.display_category = 'CASE Standards';

// InteractionType - Learner Profile
MATCH (n:InteractionType)
SET n.display_color = '#7C3AED',
    n.display_icon = 'lightbulb',
    n.display_category = 'Learner Profile';

// ContentGuideline - Learner Profile
MATCH (n:ContentGuideline)
SET n.display_color = '#7C3AED',
    n.display_icon = 'document',
    n.display_category = 'Learner Profile';

// PedagogyProfile - Learner Profile
MATCH (n:PedagogyProfile)
SET n.display_color = '#7C3AED',
    n.display_icon = 'route',
    n.display_category = 'Learner Profile';

// FeedbackProfile - Learner Profile
MATCH (n:FeedbackProfile)
SET n.display_color = '#7C3AED',
    n.display_icon = 'speech',
    n.display_category = 'Learner Profile';

// PedagogyTechnique - Learner Profile
MATCH (n:PedagogyTechnique)
SET n.display_color = '#3B0764',
    n.display_icon = 'brain',
    n.display_category = 'Learner Profile';

// DifficultyLevel - UK Curriculum
MATCH (n:DifficultyLevel)
SET n.display_color = '#E11D48',
    n.display_icon = 'signal_cellular_alt',
    n.display_category = 'UK Curriculum';

// RepresentationStage - UK Curriculum
MATCH (n:RepresentationStage)
SET n.display_color = '#06B6D4',
    n.display_icon = 'view_carousel',
    n.display_category = 'UK Curriculum';

// ThinkingLens - UK Curriculum
MATCH (n:ThinkingLens)
SET n.display_color = '#7C3AED',
    n.display_icon = 'psychology',
    n.display_category = 'UK Curriculum';

// VehicleTemplate - Vehicle Template
MATCH (n:VehicleTemplate)
SET n.display_color = '#0891B2',
    n.display_category = 'Vehicle Template';

// HistoryStudy - Topic Suggestion
MATCH (n:HistoryStudy)
SET n.display_color = '#B45309',
    n.display_icon = 'auto_stories',
    n.display_category = 'Topic Suggestion';

// DisciplinaryConcept - Subject Reference
MATCH (n:DisciplinaryConcept)
SET n.display_color = '#78350F',
    n.display_icon = 'psychology',
    n.display_category = 'Subject Reference';

// HistoricalSource - Subject Reference
MATCH (n:HistoricalSource)
SET n.display_color = '#A16207',
    n.display_icon = 'source',
    n.display_category = 'Subject Reference';

// GeoStudy - Topic Suggestion
MATCH (n:GeoStudy)
SET n.display_color = '#059669',
    n.display_icon = 'public',
    n.display_category = 'Topic Suggestion';

// GeoPlace - Subject Reference
MATCH (n:GeoPlace)
SET n.display_color = '#047857',
    n.display_icon = 'place',
    n.display_category = 'Subject Reference';

// GeoContrast - Subject Reference
MATCH (n:GeoContrast)
SET n.display_color = '#065F46',
    n.display_icon = 'compare_arrows',
    n.display_category = 'Subject Reference';

// ScienceEnquiry - Topic Suggestion
MATCH (n:ScienceEnquiry)
SET n.display_color = '#14B8A6',
    n.display_icon = 'science',
    n.display_category = 'Topic Suggestion';

// EnquiryType - Subject Reference
MATCH (n:EnquiryType)
SET n.display_color = '#0F766E',
    n.display_icon = 'biotech',
    n.display_category = 'Subject Reference';

// Misconception - Subject Reference
MATCH (n:Misconception)
SET n.display_color = '#DC2626',
    n.display_icon = 'warning',
    n.display_category = 'Subject Reference';

// EnglishUnit - Topic Suggestion
MATCH (n:EnglishUnit)
SET n.display_color = '#EC4899',
    n.display_icon = 'menu_book',
    n.display_category = 'Topic Suggestion';

// Genre - Subject Reference
MATCH (n:Genre)
SET n.display_color = '#BE185D',
    n.display_icon = 'style',
    n.display_category = 'Subject Reference';

// SetText - Subject Reference
MATCH (n:SetText)
SET n.display_color = '#9D174D',
    n.display_icon = 'auto_stories',
    n.display_category = 'Subject Reference';

// MathsManipulative - Subject Reference
MATCH (n:MathsManipulative)
SET n.display_color = '#F59E0B',
    n.display_icon = 'extension',
    n.display_category = 'Subject Reference';

// MathsRepresentation - Subject Reference
MATCH (n:MathsRepresentation)
SET n.display_color = '#D97706',
    n.display_icon = 'palette',
    n.display_category = 'Subject Reference';

// MathsContext - Subject Reference
MATCH (n:MathsContext)
SET n.display_color = '#B45309',
    n.display_icon = 'category',
    n.display_category = 'Subject Reference';

// ReasoningPromptType - Subject Reference
MATCH (n:ReasoningPromptType)
SET n.display_color = '#92400E',
    n.display_icon = 'chat',
    n.display_category = 'Subject Reference';

// ArtTopicSuggestion - Topic Suggestion
MATCH (n:ArtTopicSuggestion)
SET n.display_color = '#F97316',
    n.display_icon = 'palette',
    n.display_category = 'Topic Suggestion';

// MusicTopicSuggestion - Topic Suggestion
MATCH (n:MusicTopicSuggestion)
SET n.display_color = '#A855F7',
    n.display_icon = 'music_note',
    n.display_category = 'Topic Suggestion';

// DTTopicSuggestion - Topic Suggestion
MATCH (n:DTTopicSuggestion)
SET n.display_color = '#64748B',
    n.display_icon = 'build',
    n.display_category = 'Topic Suggestion';

// ComputingTopicSuggestion - Topic Suggestion
MATCH (n:ComputingTopicSuggestion)
SET n.display_color = '#4F46E5',
    n.display_icon = 'computer',
    n.display_category = 'Topic Suggestion';

// TopicSuggestion - Topic Suggestion
MATCH (n:TopicSuggestion)
SET n.display_color = '#059669',
    n.display_icon = 'lightbulb',
    n.display_category = 'Topic Suggestion';

// OakUnit - Oak Content
MATCH (n:OakUnit)
SET n.display_color = '#16A34A',
    n.display_icon = 'collections_bookmark',
    n.display_category = 'Oak Content';

// OakLesson - Oak Content
MATCH (n:OakLesson)
SET n.display_color = '#22C55E',
    n.display_icon = 'play_lesson',
    n.display_category = 'Oak Content';
