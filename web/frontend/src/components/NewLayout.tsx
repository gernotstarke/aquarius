import React from 'react';
import Sidebar from './Sidebar';
import Breadcrumbs from './Breadcrumbs';

interface LayoutProps {
  children: React.ReactNode;
}

const NewLayout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="flex min-h-screen bg-neutral-50">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <main className="flex-1 p-8">
          <Breadcrumbs />
          <div className="max-w-7xl">
            {children}
          </div>
        </main>
        <footer className="bg-neutral-100 border-t border-neutral-200 mt-auto py-4 px-8">
          <div className="max-w-7xl text-center text-neutral-600 text-sm">
            <p>
              Made with 🏊 in Cologne | 
              <a 
                href="https://github.com/gernotstarke/aquarius/blob/main/LICENSE" 
                target="_blank" 
                rel="noopener noreferrer"
                className="ml-1 text-primary-600 hover:text-primary-700 hover:underline"
              >
                MIT License
              </a>
            </p>
          </div>
        </footer>
      </div>
    </div>
  );
};

export default NewLayout;
