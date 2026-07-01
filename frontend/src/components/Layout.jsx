import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import ErrorBoundary from './ErrorBoundary'

const Layout = () => {
  return (
    <div className="flex min-h-screen bg-slate-50">
      <Sidebar />
      <main className="flex-1 md:ml-64">
        <div className="p-4 md:p-8">
          <ErrorBoundary>
            <Outlet />
          </ErrorBoundary>
        </div>
      </main>
    </div>
  )
}

export default Layout
