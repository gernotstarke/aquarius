import React from 'react';
import Sidebar from './Sidebar';
import Breadcrumbs from './Breadcrumbs';
import UserMenu from './UserMenu';

interface LayoutProps {
  children: React.ReactNode;
}

const NewLayout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="flex min-h-screen bg-neutral-50">
      <Sidebar />
      <main className="flex-1">
        {/* Top Navigation Bar */}
        <div className="flex items-center justify-between bg-white border-b border-gray-200 px-8 py-4">
          <Breadcrumbs />
          <UserMenu />
        </div>
        
        {/* Main Content Area */}
        <div className="p-8">
          <div className="max-w-7xl">
            {children}
          </div>
        </div>
      </main>
    </div>
  );
};

export default NewLayout;
