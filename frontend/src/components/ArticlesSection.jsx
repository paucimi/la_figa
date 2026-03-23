import articleBody from '@/assets/article-bodyart.jpg';
import articleIntimacy from '@/assets/article-intimacy.jpg';
import articleEmpowerment from '@/assets/article-empowerment.jpg';

const articles = [
  {
    image: articleBody,
    category: 'Cuerpo & Diversidad',
    title: 'Reescribiendo el Lienzo: Cuerpos Diversos como Arte Vivo',
    excerpt: 'Una exploración de cómo la diversidad corporal transforma los estándares de belleza a través de la expresión artística y el diálogo cultural.',
    delay: '0s',
  },
  {
    image: articleIntimacy,
    category: 'Intimidad & Conexión',
    title: 'El Lenguaje del Tacto en la Era Digital',
    excerpt: 'Investigamos los matices de la conexión física y cómo la tecnología tiende puentes y a la vez transforma los vínculos íntimos.',
    delay: '0.12s',
  },
  {
    image: articleEmpowerment,
    category: 'Empoderamiento',
    title: 'Futuros Luminosos: El Poder Femenino Reconfigurado',
    excerpt: 'Trazamos el paisaje evolutivo de la agencia femenina, desde la supresión histórica hasta una nueva era de liberación tecnológica.',
    delay: '0.24s',
  },
];

const ArticlesSection = () => {
  return (
    <section className="py-20 px-6">
      <div className="text-center mb-16">
        <p className="text-[9px] tracking-[0.6em] uppercase text-muted-foreground font-body mb-3">
          Artículos Curados por IA
        </p>
        <h2 className="font-display text-4xl md:text-5xl tracking-[0.15em] gold-gradient-text" style={{ lineHeight: '1' }}>
          Artículos Destacados
        </h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-10 max-w-6xl mx-auto">
        {articles.map((article) => (
          <article key={article.title} className="group cursor-pointer animate-fade-up" style={{ animationDelay: article.delay }}>
            <div className="relative overflow-hidden mb-6">
              <img src={article.image} alt={article.title} className="w-full h-72 object-cover transition-transform duration-700 group-hover:scale-105" />
              <div className="absolute inset-0 bg-gradient-to-t from-black/30 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
            </div>
            <p className="text-[9px] tracking-[0.5em] uppercase text-primary font-body mb-3 font-medium">{article.category}</p>
            <h3 className="font-editorial text-xl md:text-2xl font-light text-foreground mb-3 group-hover:text-primary transition-colors duration-300" style={{ lineHeight: '1.25' }}>
              {article.title}
            </h3>
            <p className="text-xs font-body font-light text-muted-foreground leading-relaxed">{article.excerpt}</p>
          </article>
        ))}
      </div>
    </section>
  );
};

export default ArticlesSection;
