import { BarChart3, FileText, Share2, Users } from 'lucide-react';

const modules = [
  {
    icon: BarChart3,
    title: 'Tendencias & Investigación IA',
    description: 'Flujos de datos en tiempo real, análisis del pulso cultural y mapeo abstracto de tendencias',
    delay: '0s',
  },
  {
    icon: FileText,
    title: 'Generación de Contenido IA',
    description: 'Redacción editorial estilizada, calibración de voz autoral y síntesis narrativa',
    delay: '0.1s',
  },
  {
    icon: Share2,
    title: 'Distribución IA',
    description: 'Orquestación multiplataforma, segmentación de audiencias y sindicación multicanal',
    delay: '0.2s',
  },
  {
    icon: Users,
    title: 'Comunidad & Diálogo IA',
    description: 'Analítica de interacción, mapeo de sentimiento y facilitación de diálogo inclusivo',
    delay: '0.3s',
  },
];

const AIModulesSection = () => {
  return (
    <section className="relative py-16 px-6">
      <div className="text-center mb-12">
        <p className="text-[10px] tracking-[0.5em] uppercase text-muted-foreground font-body mb-2">
          Pipeline Editorial
        </p>
        <h2
          className="font-display text-3xl md:text-4xl tracking-[0.1em] gold-gradient-text"
          style={{ lineHeight: '1.1' }}
        >
          Red de Agentes IA
        </h2>
      </div>

      <div className="hidden lg:block absolute inset-0 pointer-events-none">
        <svg className="w-full h-full" viewBox="0 0 1200 400" fill="none" xmlns="http://www.w3.org/2000/svg">
          <line x1="300" y1="200" x2="600" y2="200" stroke="hsla(43, 40%, 22%, 0.4)" strokeWidth="1" strokeDasharray="4 4" />
          <line x1="600" y1="200" x2="900" y2="200" stroke="hsla(43, 40%, 22%, 0.4)" strokeWidth="1" strokeDasharray="4 4" />
          <line x1="450" y1="100" x2="600" y2="200" stroke="hsla(43, 40%, 22%, 0.3)" strokeWidth="1" strokeDasharray="4 4" />
          <line x1="750" y1="100" x2="600" y2="200" stroke="hsla(43, 40%, 22%, 0.3)" strokeWidth="1" strokeDasharray="4 4" />
        </svg>
      </div>

      <div className="relative grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
        {modules.map((mod) => (
          <div
            key={mod.title}
            className="module-panel p-6 rounded-sm group hover:border-primary/40 transition-all duration-500 animate-fade-up"
            style={{ animationDelay: mod.delay }}
          >
            <mod.icon className="w-5 h-5 text-primary mb-4 group-hover:drop-shadow-[0_0_8px_hsla(43,72%,55%,0.5)] transition-all duration-300" />
            <h3 className="font-display text-sm tracking-[0.15em] text-primary mb-3" style={{ lineHeight: '1.2' }}>
              {mod.title}
            </h3>
            <p className="text-xs font-body font-light text-muted-foreground leading-relaxed">
              {mod.description}
            </p>
            <div className="mt-4 flex items-center gap-1.5">
              {[...Array(5)].map((_, i) => (
                <div
                  key={i}
                  className="h-1 rounded-full bg-primary/20 group-hover:bg-primary/50 transition-colors duration-500"
                  style={{ width: `${14 + i * 4}px`, transitionDelay: `${i * 60}ms` }}
                />
              ))}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default AIModulesSection;
