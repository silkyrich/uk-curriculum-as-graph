// Display Properties Migration
// Auto-generated styling for UK Curriculum Knowledge Graph
// Color scheme: Tailwind CSS palette
// Icons: Material Design icon names

// Curriculum - Structure
MATCH (n:Curriculum)
SET n.display_color = '#1F2937',
    n.display_icon = 'account_balance',
    n.display_category = 'Structure',
    n.display_size = 5;

// KeyStage - Structure
MATCH (n:KeyStage)
SET n.display_color = '#374151',
    n.display_icon = 'stairs',
    n.display_category = 'Structure',
    n.display_size = 5;

// Year - Structure
MATCH (n:Year)
SET n.display_color = '#4B5563',
    n.display_icon = 'event',
    n.display_category = 'Structure',
    n.display_size = 4;

// Subject - UK Curriculum
MATCH (n:Subject)
SET n.display_color = '#DC2626',
    n.display_icon = 'menu_book',
    n.display_category = 'UK Curriculum',
    n.display_size = 4;

// Programme - UK Curriculum
MATCH (n:Programme)
SET n.display_color = '#1E3A8A',
    n.display_icon = 'assignment',
    n.display_category = 'UK Curriculum',
    n.display_size = 4;

// Domain - UK Curriculum
MATCH (n:Domain)
SET n.display_color = '#8B5CF6',
    n.display_icon = 'folder',
    n.display_category = 'UK Curriculum',
    n.display_size = 3;

// Topic - UK Curriculum
MATCH (n:Topic)
SET n.display_color = '#7C3AED',
    n.display_icon = 'history_edu',
    n.display_category = 'UK Curriculum',
    n.display_size = 3;

// Objective - UK Curriculum
MATCH (n:Objective)
SET n.display_color = '#10B981',
    n.display_icon = 'flag',
    n.display_category = 'UK Curriculum',
    n.display_size = 2;

// Concept - UK Curriculum
MATCH (n:Concept)
SET n.display_color = '#3B82F6',
    n.display_icon = 'lightbulb_outline',
    n.display_category = 'UK Curriculum',
    n.display_size = 2;

// ConceptCluster - UK Curriculum
MATCH (n:ConceptCluster)
SET n.display_color = '#6366F1',
    n.display_icon = 'view_module',
    n.display_category = 'UK Curriculum',
    n.display_size = 2;

// SourceDocument - Structure
MATCH (n:SourceDocument)
SET n.display_color = '#6B7280',
    n.display_icon = 'description',
    n.display_category = 'Structure',
    n.display_size = 1;

// WorkingScientifically - Epistemic Skills
MATCH (n:WorkingScientifically)
SET n.display_color = '#14B8A6',
    n.display_icon = 'science',
    n.display_category = 'Epistemic Skills',
    n.display_size = 2;

// ReadingSkill - Epistemic Skills
MATCH (n:ReadingSkill)
SET n.display_color = '#EC4899',
    n.display_icon = 'menu_book',
    n.display_category = 'Epistemic Skills',
    n.display_size = 2;

// MathematicalReasoning - Epistemic Skills
MATCH (n:MathematicalReasoning)
SET n.display_color = '#F59E0B',
    n.display_icon = 'calculate',
    n.display_category = 'Epistemic Skills',
    n.display_size = 2;

// GeographicalSkill - Epistemic Skills
MATCH (n:GeographicalSkill)
SET n.display_color = '#059669',
    n.display_icon = 'public',
    n.display_category = 'Epistemic Skills',
    n.display_size = 2;

// HistoricalThinking - Epistemic Skills
MATCH (n:HistoricalThinking)
SET n.display_color = '#92400E',
    n.display_icon = 'history_edu',
    n.display_category = 'Epistemic Skills',
    n.display_size = 2;

// ComputationalThinking - Epistemic Skills
MATCH (n:ComputationalThinking)
SET n.display_color = '#4F46E5',
    n.display_icon = 'computer',
    n.display_category = 'Epistemic Skills',
    n.display_size = 2;

// TestFramework - Assessment
MATCH (n:TestFramework)
SET n.display_color = '#374151',
    n.display_icon = 'quiz',
    n.display_category = 'Assessment',
    n.display_size = 4;

// TestPaper - Assessment
MATCH (n:TestPaper)
SET n.display_color = '#4B5563',
    n.display_icon = 'description',
    n.display_category = 'Assessment',
    n.display_size = 1;

// ContentDomainCode - Assessment
MATCH (n:ContentDomainCode)
SET n.display_color = '#6B7280',
    n.display_icon = 'bookmark',
    n.display_category = 'Assessment',
    n.display_size = 1;

// Framework - CASE Standards
MATCH (n:Framework)
SET n.display_color = '#EA580C',
    n.display_icon = 'account_balance',
    n.display_category = 'CASE Standards',
    n.display_size = 5;

// Dimension - CASE Standards
MATCH (n:Dimension)
SET n.display_color = '#C2410C',
    n.display_icon = 'view_in_ar',
    n.display_category = 'CASE Standards',
    n.display_size = 4;

// CoreIdea - CASE Standards
MATCH (n:CoreIdea)
SET n.display_color = '#B45309',
    n.display_icon = 'school',
    n.display_category = 'CASE Standards',
    n.display_size = 3;

// CrosscuttingConcept - CASE Standards
MATCH (n:CrosscuttingConcept)
SET n.display_color = '#15803D',
    n.display_icon = 'hub',
    n.display_category = 'CASE Standards',
    n.display_size = 2;

// Practice - CASE Standards
MATCH (n:Practice)
SET n.display_color = '#0284C7',
    n.display_icon = 'engineering',
    n.display_category = 'CASE Standards',
    n.display_size = 2;

// PerformanceExpectation - CASE Standards
MATCH (n:PerformanceExpectation)
SET n.display_color = '#6B7280',
    n.display_icon = 'assessment',
    n.display_category = 'CASE Standards',
    n.display_size = 1;

// GradeBand - CASE Standards
MATCH (n:GradeBand)
SET n.display_color = '#9CA3AF',
    n.display_icon = 'grade',
    n.display_category = 'CASE Standards',
    n.display_size = 1;

// MathPractice - CASE Standards
MATCH (n:MathPractice)
SET n.display_color = '#D97706',
    n.display_icon = 'functions',
    n.display_category = 'CASE Standards',
    n.display_size = 2;

// InteractionType - Learner Profile
MATCH (n:InteractionType)
SET n.display_color = '#7C3AED',
    n.display_icon = 'lightbulb',
    n.display_category = 'Learner Profile',
    n.display_size = 2;

// ContentGuideline - Learner Profile
MATCH (n:ContentGuideline)
SET n.display_color = '#7C3AED',
    n.display_icon = 'document',
    n.display_category = 'Learner Profile',
    n.display_size = 3;

// PedagogyProfile - Learner Profile
MATCH (n:PedagogyProfile)
SET n.display_color = '#7C3AED',
    n.display_icon = 'route',
    n.display_category = 'Learner Profile',
    n.display_size = 3;

// FeedbackProfile - Learner Profile
MATCH (n:FeedbackProfile)
SET n.display_color = '#7C3AED',
    n.display_icon = 'speech',
    n.display_category = 'Learner Profile',
    n.display_size = 3;

// PedagogyTechnique - Learner Profile
MATCH (n:PedagogyTechnique)
SET n.display_color = '#3B0764',
    n.display_icon = 'brain',
    n.display_category = 'Learner Profile',
    n.display_size = 3;

// DifficultyLevel - UK Curriculum
MATCH (n:DifficultyLevel)
SET n.display_color = '#F59E0B',
    n.display_icon = 'signal_cellular_alt',
    n.display_category = 'UK Curriculum',
    n.display_size = 1;

// RepresentationStage - UK Curriculum
MATCH (n:RepresentationStage)
SET n.display_color = '#06B6D4',
    n.display_icon = 'view_carousel',
    n.display_category = 'UK Curriculum',
    n.display_size = 1;

// ThinkingLens - UK Curriculum
MATCH (n:ThinkingLens)
SET n.display_color = '#7C3AED',
    n.display_icon = 'psychology',
    n.display_category = 'UK Curriculum',
    n.display_size = 2;

// ContentVehicle - Content Vehicle
MATCH (n:ContentVehicle)
SET n.display_color = '#0D9488',
    n.display_icon = 'local_library',
    n.display_category = 'Content Vehicle',
    n.display_size = 2;

// OakUnit - Oak Content
MATCH (n:OakUnit)
SET n.display_color = '#16A34A',
    n.display_icon = 'collections_bookmark',
    n.display_category = 'Oak Content',
    n.display_size = 3;

// OakLesson - Oak Content
MATCH (n:OakLesson)
SET n.display_color = '#22C55E',
    n.display_icon = 'play_lesson',
    n.display_category = 'Oak Content',
    n.display_size = 2;
