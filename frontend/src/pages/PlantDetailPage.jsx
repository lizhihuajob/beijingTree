import { Link, useParams, useNavigate } from 'react-router-dom'
import { getPlantById, formatProtectionStatus } from '../utils/plantUtils'

function PlantDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const plant = getPlantById(id)

  if (!plant) {
    return (
      <div className="min-h-screen bg-gray-50 py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="text-6xl mb-4">🌱</div>
          <h2 className="text-2xl font-bold text-gray-700 mb-4">
            未找到该植物
          </h2>
          <p className="text-gray-500 mb-6">
            您访问的植物信息不存在
          </p>
          <Link
            to="/plants"
            className="inline-flex items-center px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            ← 返回植物列表
          </Link>
        </div>
      </div>
    )
  }

  const protection = formatProtectionStatus(plant.protection_status)

  const handleBack = () => {
    navigate(-1)
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <button
          onClick={handleBack}
          className="inline-flex items-center text-gray-600 hover:text-primary-600 mb-6 transition-colors"
        >
          <span className="mr-2">←</span>
          返回
        </button>

        <div className="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-100">
          <div className="h-64 md:h-80 bg-gradient-to-br from-primary-100 via-primary-50 to-primary-100 flex items-center justify-center">
            <span className="text-8xl md:text-9xl">🌿</span>
          </div>

          <div className="p-6 md:p-8">
            <div className="flex flex-col md:flex-row md:items-start md:justify-between mb-6">
              <div>
                <div className="flex items-center space-x-3 mb-2">
                  <h1 className="text-3xl font-bold text-gray-900">
                    {plant.name_cn}
                  </h1>
                  {protection && (
                    <span className={`protection-badge px-3 py-1 rounded-full text-sm ${protection.color}`}>
                      {protection.text}
                    </span>
                  )}
                </div>
                <p className="text-lg text-gray-500 italic">
                  {plant.name_latin}
                </p>
              </div>
            </div>

            {plant.description && (
              <div className="mb-8">
                <h2 className="text-xl font-semibold text-gray-900 mb-3 flex items-center">
                  <span className="mr-2">📝</span>
                  植物描述
                </h2>
                <p className="text-gray-700 leading-relaxed bg-gray-50 p-4 rounded-lg">
                  {plant.description}
                </p>
              </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
              <div className="bg-primary-50 p-4 rounded-lg">
                <h3 className="text-sm font-medium text-primary-800 mb-2">
                  🌳 分类信息
                </h3>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-600">科：</span>
                    <span className="font-medium text-gray-900">{plant.family}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">属：</span>
                    <span className="font-medium text-gray-900">{plant.genus}</span>
                  </div>
                </div>
              </div>

              {plant.habitat && (
                <div className="bg-blue-50 p-4 rounded-lg">
                  <h3 className="text-sm font-medium text-blue-800 mb-2">
                    🌍 生态习性
                  </h3>
                  <p className="text-gray-700">{plant.habitat}</p>
                </div>
              )}

              {plant.distribution && (
                <div className="bg-green-50 p-4 rounded-lg">
                  <h3 className="text-sm font-medium text-green-800 mb-2">
                    🗺️ 地理分布
                  </h3>
                  <p className="text-gray-700">{plant.distribution}</p>
                </div>
              )}

              {plant.garden_zones && plant.garden_zones.length > 0 && (
                <div className="bg-orange-50 p-4 rounded-lg">
                  <h3 className="text-sm font-medium text-orange-800 mb-2">
                    🏛️ 园区分布
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {plant.garden_zones.map((zone, index) => (
                      <Link
                        key={index}
                        to={`/plants?zone=${encodeURIComponent(zone)}`}
                        className="px-3 py-1 bg-white text-orange-700 rounded-full text-sm hover:bg-orange-100 transition-colors"
                      >
                        {zone}
                      </Link>
                    ))}
                  </div>
                </div>
              )}
            </div>

            <div className="border-t pt-6">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between text-sm text-gray-500">
                <div>
                  <span>数据来源：{plant.source_url || '北京植物园'}</span>
                </div>
                {plant.collected_at && (
                  <div className="mt-2 sm:mt-0">
                    <span>采集时间：{plant.collected_at}</span>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        <div className="mt-8 flex justify-center space-x-4">
          <Link
            to="/plants"
            className="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            浏览全部植物
          </Link>
          <Link
            to="/"
            className="px-6 py-3 bg-white text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
          >
            返回首页
          </Link>
        </div>
      </div>
    </div>
  )
}

export default PlantDetailPage
