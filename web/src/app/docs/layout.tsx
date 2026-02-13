'use client';

import { usePathname } from 'next/navigation';
import { useEffect } from 'react';
import Link from 'next/link';
import { 
  Book, 
  Mic, 
  Brain, 
  Route, 
  Code, 
  Terminal, 
  Download,
  Home,
  Layers,
  Server,
  ChevronRight,
  Github,
  ArrowLeft,
  Lightbulb,
  BarChart3,
  Database
} from 'lucide-react';

const navigation = [
  {
    title: 'Pour commencer',
    items: [
      { title: 'Introduction', href: '/docs', icon: Book },
      { title: 'Installation', href: '/docs/installation', icon: Download },
      { title: 'Démarrage rapide', href: '/docs/quickstart', icon: Terminal },
    ]
  },
  {
    title: 'Pipeline',
    items: [
      { title: 'Vue d\'ensemble', href: '/docs/pipeline', icon: Layers },
      { title: 'STT (Whisper)', href: '/docs/stt', icon: Mic },
      { title: 'NLP (spaCy)', href: '/docs/nlp', icon: Brain },
      { title: 'Pathfinding', href: '/docs/pathfinding', icon: Route },
    ]
  },
  {
    title: 'API & CLI',
    items: [
      { title: 'API REST', href: '/docs/api', icon: Server },
      { title: 'Commandes CLI', href: '/docs/cli', icon: Code },
    ]
  },
  {
    title: 'Recherche',
    items: [
      { title: 'Benchmarks', href: '/docs/benchmarks', icon: BarChart3 },
      { title: 'Datasets', href: '/docs/datasets', icon: Database },
      { title: 'Améliorations', href: '/docs/improvements', icon: Lightbulb },
    ]
  }
];

const allPages = navigation.flatMap(section => section.items);

export default function DocsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [pathname]);
  
  const currentIndex = allPages.findIndex(page => page.href === pathname);
  const prevPage = currentIndex > 0 ? allPages[currentIndex - 1] : null;
  const nextPage = currentIndex < allPages.length - 1 ? allPages[currentIndex + 1] : null;

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white">
      <header className="fixed top-0 left-0 right-0 z-50 bg-[#0a0a0a]/95 backdrop-blur-md border-b border-white/5">
        <div className="max-w-[1400px] mx-auto px-6 h-14 flex items-center justify-between">
          <div className="flex items-center gap-6">
            <Link href="/" className="flex items-center gap-2 text-neutral-400 hover:text-white transition-colors text-sm">
              <ArrowLeft className="w-4 h-4" />
              <span className="hidden sm:inline">Retour à l'app</span>
            </Link>
            <div className="h-4 w-px bg-white/10" />
            <Link href="/docs" className="flex items-center gap-2">
              <span className="font-semibold">THOR</span>
              <span className="text-neutral-500 text-sm">Docs</span>
            </Link>
          </div>
          
          <div className="flex items-center gap-4">
            <span className="text-xs text-neutral-500 hidden md:block">v1.0.0</span>
            <a 
              href="https://github.com/THOR-EPITECH/THOR" 
              target="_blank" 
              rel="noopener noreferrer"
              className="p-2 text-neutral-500 hover:text-white transition-colors"
            >
              <Github className="w-4 h-4" />
            </a>
          </div>
        </div>
      </header>

      <div className="flex pt-14">
        <aside className="hidden lg:block w-64 fixed left-0 top-14 bottom-0 overflow-y-auto border-r border-white/5 bg-[#0a0a0a]">
          <nav className="p-6 space-y-8">
            {navigation.map((section) => (
              <div key={section.title}>
                <h3 className="text-xs font-semibold text-neutral-500 uppercase tracking-wider mb-3">
                  {section.title}
                </h3>
                <ul className="space-y-1">
                  {section.items.map((item) => {
                    const isActive = pathname === item.href;
                    const Icon = item.icon;
                    return (
                      <li key={item.href}>
                        <Link
                          href={item.href}
                          className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-all ${
                            isActive
                              ? 'bg-white/10 text-white'
                              : 'text-neutral-400 hover:text-white hover:bg-white/5'
                          }`}
                        >
                          <Icon className="w-4 h-4" />
                          {item.title}
                        </Link>
                      </li>
                    );
                  })}
                </ul>
              </div>
            ))}
          </nav>
        </aside>

        <div className="lg:hidden fixed top-14 left-0 right-0 z-40 bg-[#0a0a0a] border-b border-white/5 overflow-x-auto">
          <nav className="flex gap-1 p-2 min-w-max">
            {allPages.map((item) => {
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`px-3 py-1.5 rounded-full text-xs whitespace-nowrap transition-all ${
                    isActive
                      ? 'bg-white text-black'
                      : 'text-neutral-400 hover:text-white hover:bg-white/5'
                  }`}
                >
                  {item.title}
                </Link>
              );
            })}
          </nav>
        </div>

        <main className="flex-1 lg:ml-64 min-h-screen">
          <div 
            key={pathname}
            className="max-w-3xl mx-auto px-6 py-12 lg:py-16 mt-12 lg:mt-0 animate-fade-in"
          >
            {children}

            <div className="mt-16 pt-8 border-t border-white/5 flex items-center justify-between">
              {prevPage ? (
                <Link
                  href={prevPage.href}
                  className="group flex flex-col items-start"
                >
                  <span className="text-xs text-neutral-500 mb-1">Précédent</span>
                  <span className="text-sm text-neutral-300 group-hover:text-white transition-colors flex items-center gap-2">
                    <ChevronRight className="w-4 h-4 rotate-180" />
                    {prevPage.title}
                  </span>
                </Link>
              ) : <div />}
              
              {nextPage ? (
                <Link
                  href={nextPage.href}
                  className="group flex flex-col items-end"
                >
                  <span className="text-xs text-neutral-500 mb-1">Suivant</span>
                  <span className="text-sm text-neutral-300 group-hover:text-white transition-colors flex items-center gap-2">
                    {nextPage.title}
                    <ChevronRight className="w-4 h-4" />
                  </span>
                </Link>
              ) : <div />}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
