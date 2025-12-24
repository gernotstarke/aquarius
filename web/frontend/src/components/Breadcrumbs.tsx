import React from 'react';
import { Link, useLocation } from 'react-router-dom';

interface BreadcrumbItem {
  label: string;
  path?: string;
}

const pathToBreadcrumbs = (pathname: string): BreadcrumbItem[] => {
  const segments = pathname.split('/').filter(Boolean);
  const breadcrumbs: BreadcrumbItem[] = [{ label: 'Home', path: '/' }];

  // Map path segments to readable labels
  const labelMap: Record<string, string> = {
    'stammdaten': 'Stammdaten',
    'saisons': 'Saisons',
    'schwimmbaeder': 'Schwimmbäder',
    'figuren': 'Figuren',
    'kinder': 'Kinder',
    'wettkaempfe': 'Wettkämpfe',
    'anmeldung': 'Anmeldung',
    'liste': 'Liste',
    'new': 'Neu',
    'basis': 'Basis',
    'stationen': 'Stationen',
    'zeitplanung': 'Zeitplanung',
    'anmeldungen': 'Anmeldungen',
  };

  let currentPath = '';
  segments.forEach((segment, index) => {
    currentPath += `/${segment}`;
    const isLast = index === segments.length - 1;

    // Skip numeric IDs in breadcrumbs
    if (/^\d+$/.test(segment)) {
      breadcrumbs.push({
        label: `#${segment}`,
        path: isLast ? undefined : currentPath,
      });
    } else {
      breadcrumbs.push({
        label: labelMap[segment] || segment,
        path: isLast ? undefined : currentPath,
      });
    }
  });

  return breadcrumbs;
};

const Breadcrumbs: React.FC = () => {
  const location = useLocation();
  const breadcrumbs = pathToBreadcrumbs(location.pathname);

  if (breadcrumbs.length <= 1) return null;

  return (
    <nav className="flex items-center gap-2 text-sm text-neutral-600 mb-6">
      {breadcrumbs.map((crumb, index) => (
        <React.Fragment key={crumb.path || crumb.label}>
          {index > 0 && <span className="text-neutral-400">›</span>}
          {crumb.path ? (
            <Link
              to={crumb.path}
              className="hover:text-primary-600 transition-colors"
            >
              {crumb.label}
            </Link>
          ) : (
            <span className="font-medium text-neutral-900">{crumb.label}</span>
          )}
        </React.Fragment>
      ))}
    </nav>
  );
};

export default Breadcrumbs;
