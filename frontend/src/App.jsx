import HeroSection from '@/components/HeroSection';
import AIModulesSection from '@/components/AIModulesSection';
import ArticlesSection from '@/components/ArticlesSection';
import FooterSection from '@/components/FooterSection';

const App = () => {
  return (
    <div className="min-h-screen bg-background relative">
      {/* Gold border frame */}
      <div className="fixed inset-0 pointer-events-none z-50">
        <div className="absolute inset-2 border border-primary/25 rounded-sm" />
      </div>

      {/* Content */}
      <div className="relative z-10 max-w-7xl mx-auto">
        <HeroSection />
        <AIModulesSection />
        <ArticlesSection />
        <FooterSection />
      </div>
    </div>
  );
};

export default App;
