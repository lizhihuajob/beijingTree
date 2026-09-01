function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="bg-gray-800 text-gray-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <div className="flex items-center space-x-2 mb-3">
              <span className="text-2xl">🌿</span>
              <h3 className="text-lg font-semibold text-white">北京植物园植物数据库</h3>
            </div>
            <p className="text-sm text-gray-400">
              展示北京植物园的植物资源信息，普及植物知识。
            </p>
          </div>

          <div>
            <h4 className="text-white font-medium mb-3">快速链接</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <a href="/" className="hover:text-white transition-colors">
                首页
              </a>
              </li>
              <li>
                <a href="/plants" className="hover:text-white transition-colors">
                植物列表
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="text-white font-medium mb-3">数据来源</h4>
            <p className="text-sm text-gray-400">
              数据来源于北京植物园相关网站及公开资料。
            </p>
          </div>
        </div>

        <div className="mt-8 pt-6 border-t border-gray-700 text-center text-sm text-gray-500">
          <p>© {currentYear} 北京植物园植物数据库 | 仅供学习和研究使用</p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
