import { Link, useLocation } from 'react-router-dom'

function Header() {
  const location = useLocation()

  const isActive = (path) => {
    if (path === '/') return location.pathname === '/'
    return location.pathname.startsWith(path)
  }

  return (
    <header className="bg-gradient-to-r from-primary-700 to-primary-600 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center space-x-3">
            <span className="text-2xl">🌿</span>
            <div>
              <h1 className="text-xl font-bold">北京植物园植物数据库</h1>
              <p className="text-xs text-primary-100 hidden sm:block">Beijing Botanical Garden</p>
            </div>
          </Link>

          <nav className="hidden md:flex items-center space-x-1">
            <Link
              to="/"
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive('/')
                  ? 'bg-primary-500 text-white'
                  : 'text-primary-100 hover:bg-primary-500 hover:text-white'
              }`}
            >
              首页
            </Link>
            <Link
              to="/plants"
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive('/plants') && location.pathname !== '/'
                  ? 'bg-primary-500 text-white'
                  : 'text-primary-100 hover:bg-primary-500 hover:text-white'
              }`}
            >
              植物列表
            </Link>
          </nav>

          <div className="md:hidden">
            <Link
              to="/"
              className={`px-3 py-2 rounded-md text-sm font-medium ${
                isActive('/') ? 'bg-primary-500 text-white' : 'text-primary-100'
              }`}
            >
              首页
            </Link>
            <Link
              to="/plants"
              className={`px-3 py-2 rounded-md text-sm font-medium ml-1 ${
                isActive('/plants') && location.pathname !== '/'
                  ? 'bg-primary-500 text-white'
                  : 'text-primary-100'
              }`}
            >
              列表
            </Link>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
