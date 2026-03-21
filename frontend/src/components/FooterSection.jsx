import { Star } from 'lucide-react';

const FooterSection = () => {
  return (
    <footer className="py-16 px-6">
      <div className="max-w-6xl mx-auto mb-12">
        <div className="h-px bg-gradient-to-r from-transparent via-border to-transparent" />
      </div>

      <div className="text-center mb-12 animate-fade-up">
        <h2 className="font-display text-2xl md:text-3xl tracking-[0.12em] gold-gradient-text mb-6" style={{ lineHeight: '1.1' }}>
          Explora el Futuro de la Sexualidad Inclusiva
        </h2>
        <button className="px-8 py-3 border border-primary/60 text-primary text-xs tracking-[0.3em] uppercase font-body font-light hover:bg-primary/10 transition-colors duration-300 active:scale-[0.97] rounded-sm">
          Entrar a la Plataforma
        </button>
      </div>

      <div className="max-w-2xl mx-auto text-center mb-12">
        <p className="text-[9px] tracking-[0.5em] uppercase text-primary font-body mb-3">
          Sobre Nuestro Proceso Impulsado por IA
        </p>
        <p className="text-xs font-editorial font-light text-muted-foreground leading-relaxed italic">
          Cada artículo, análisis de tendencias y decisión editorial en LA FIGA es orquestado por una red de
          agentes de IA especializados — desde la investigación y redacción hasta la distribución y el diálogo
          comunitario — garantizando una publicación consistentemente progresista, inclusiva y culturalmente resonante.
        </p>
      </div>

      <div className="max-w-6xl mx-auto flex items-center justify-between pt-8 border-t border-border/30">
        <p className="text-[9px] tracking-[0.4em] uppercase text-muted-foreground font-body">
          Periodismo Digital & Cultural
        </p>
        <Star className="w-3 h-3 text-primary/60" />
      </div>
    </footer>
  );
};

export default FooterSection;
