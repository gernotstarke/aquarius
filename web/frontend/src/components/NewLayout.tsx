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
      <main className="flex-1 p-8">
        <Breadcrumbs />
        <div className="max-w-7xl">
          {children}
        </div>
      </main>
    </div>
  );
};

export default NewLayout;
