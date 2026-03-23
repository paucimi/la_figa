import { useEffect, useState } from 'react';
import articleBody from '@/assets/article-bodyart.jpg';
import articleIntimacy from '@/assets/article-intimacy.jpg';
import articleEmpowerment from '@/assets/article-empowerment.jpg';

const COVER_IMAGES = [articleBody, articleIntimacy, articleEmpowerment];

const FALLBACK_ARTICLES = [
  {
    category: 'Cuerpo & Diversidad',
    titulo: 'Reescribiendo el Lienzo: Cuerpos Diversos como Arte Vivo',
    extracto: 'Una exploración de cómo la diversidad corporal transforma los estándares de belleza a través de la expresión artística y el diálogo cultural.',
  },
  {
    category: 'Intimidad & Conexión',
    titulo: 'El Lenguaje del Tacto en la Era Digital',
    extracto: 'Investigamos los matices de la conexión física y cómo la tecnología tiende puentes y a la vez transforma los vínculos íntimos.',
  },
  {
    category: 'Empoderamiento',
    titulo: 'Futuros Luminosos: El Poder Femenino Reconfigurado',
    extracto: 'Trazamos el paisaje evolutivo de la agencia femenina, desde la supresión histórica hasta una nueva era de liberación tecnológica.',
  },
];

const ArticlesSection = () => {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/articles')
      .then((r) => r.json())
      .then((data) => {
        setArticles(Array.isArray(data) && data.length > 0 ? data.slice(0, 3) : FALLBACK_ARTICLES);
      })
      .catch(() => setArticles(FALLBACK_ARTICLES))
      .finally(() => setLoading(false));
  }, []);

  const displayArticles = loading ? FALLBACK_ARTICLES : articles;

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
        {displayArticles.map((article, idx) => (
          <article
            key={article.id || article.titulo}
            className="group cursor-pointer animate-fade-up"
            style={{ animationDelay: `${idx * 0.12}s` }}
            onClick={() => article.id && (window.location.href = `/editor#${article.id}`)}
          >
            <div className="relative overflow-hidden mb-6">
              <img
                src={COVER_IMAGES[idx % COVER_IMAGES.length]}
                alt={article.titulo}
                className="w-full h-72 object-cover transition-transform duration-700 group-hover:scale-105"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
            </div>
            <p className="text-[9px] tracking-[0.5em] uppercase text-primary font-body mb-3 font-medium">
              {article.tema || article.category || 'La Figa'}
            </p>
            <h3
              className="font-editorial text-xl md:text-2xl font-light text-foreground mb-3 group-hover:text-primary transition-colors duration-300"
              style={{ lineHeight: '1.25' }}
            >
              {article.titulo}
            </h3>
            <p className="text-xs font-body font-light text-muted-foreground leading-relaxed">
              {article.extracto}
            </p>
            {article.fecha && (
              <p className="mt-4 text-[9px] tracking-[0.3em] uppercase text-muted-foreground/50 font-body">
                {article.fecha}
              </p>
            )}
          </article>
        ))}
      </div>
    </section>
  );
};

export default ArticlesSection;
