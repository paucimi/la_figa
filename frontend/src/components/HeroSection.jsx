import lotusEmblem from '@/assets/lotus-emblem.png';

const HeroSection = () => {
  return (
    <section className="relative flex flex-col items-center pt-16 pb-12 px-6">
      <h1
        className="font-display text-6xl md:text-8xl lg:text-9xl tracking-[0.15em] gold-gradient-text gold-glow-text animate-fade-up"
        style={{ lineHeight: '0.95' }}
      >
        LA FIGA
      </h1>

      <p
        className="mt-6 text-center text-xs md:text-sm tracking-[0.3em] uppercase text-gold-light font-body font-light animate-fade-up"
        style={{ animationDelay: '0.15s' }}
      >
        Una Plataforma Editorial Impulsada por IA para la Sexualidad Femenina. (Vol. 1 | 2026)
      </p>

      <p
        className="mt-3 text-center text-[10px] md:text-xs tracking-[0.4em] uppercase text-muted-foreground font-body animate-fade-up"
        style={{ animationDelay: '0.3s' }}
      >
        Revolucionando el Periodismo Digital. Rompiendo Tabúes.
      </p>

      <div
        className="mt-8 w-24 h-px bg-gradient-to-r from-transparent via-primary to-transparent animate-fade-in"
        style={{ animationDelay: '0.4s' }}
      />

      <div className="relative mt-10 animate-fade-up" style={{ animationDelay: '0.5s' }}>
        <div className="absolute inset-0 rounded-full animate-gold-pulse gold-glow" />
        <img
          src={lotusEmblem}
          alt="Emblema del loto cibernético dorado — LA FIGA"
          className="relative w-64 h-64 md:w-80 md:h-80 lg:w-96 lg:h-96 object-contain"
        />
      </div>
    </section>
  );
};

export default HeroSection;
