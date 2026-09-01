import { useState, useEffect } from 'react'
import { Link, useParams, useNavigate } from 'react-router-dom'
import { getPlantById, formatProtectionStatus } from '../utils/plantUtils'

function PlantDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [plant, setPlant] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadPlant = async () => {
      setLoading(true)
      try {
        const data = await getPlantById(id)
        setPlant(data)
      } catch (error) {
        console.error('Failed to load plant:', error)
      } finally {
        setLoading(false)
      }
    }
    loadPlant()
  }, [id])

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="text-6xl mb-4">🌿</div>
          <div className="text-gray-500">加载中...</div>
        </div>
      </div>
    )
  }

  if (!plant || plant.error) {
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
  const hasImage = plant.primary_image && plant.primary_image.length > 0

  const handleBack = () => {
    navigate(-1)
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <button
          onClick={handleBack}
          className="inline-flex items-center text-gray-600 hover:text-primary-600 mb-6 transition-colors"
        >
          <span className="mr-2">←</span>
          返回
        </button>

        <div className="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-100">
          <div className="relative h-64 md:h-96 bg-gradient-to-br from-primary-100 via-primary-50 to-primary-100 overflow-hidden">
            {hasImage ? (
              <img
                src={plant.primary_image}
                alt={plant.name_cn}
                className="w-full h-full object-cover"
                onError={(e) => {
                  e.target.style.display = 'none'
                  e.target.nextSibling.style.display = 'flex'
                }}
              />
            ) : null}
            <div className={`${hasImage ? 'hidden' : 'flex'} w-full h-full items-center justify-center`}>
              <span className="text-8xl md:text-9xl">🌿</span>
            </div>
            
            <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/60 to-transparent p-6">
              <div className="flex flex-col md:flex-row md:items-end md:justify-between">
                <div>
                  <div className="flex items-center space-x-3 mb-2">
                    <h1 className="text-3xl md:text-4xl font-bold text-white">
                      {plant.name_cn}
                    </h1>
                    {protection && (
                      <span className={`protection-badge px-3 py-1 rounded-full text-sm shadow ${protection.color}`}>
                        {protection.text}
                      </span>
                    )}
                  </div>
                  <p className="text-lg text-gray-200 italic">
                    {plant.name_latin}
                  </p>
                </div>
                <div className="mt-4 md:mt-0">
                  {plant.common_names && plant.common_names.length > 0 && (
                    <div className="flex flex-wrap gap-2">
                      {plant.common_names.map((name, index) => (
                        <span key={index} className="text-xs px-3 py-1 bg-white/20 text-white rounded-full backdrop-blur-sm">
                          {name}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>

          <div className="p-6 md:p-8">
            {plant.description && (
              <div className="mb-8">
                <h2 className="text-xl font-semibold text-gray-900 mb-3 flex items-center">
                  <span className="mr-2">📝</span>
                  植物简介
                </h2>
                <p className="text-gray-700 leading-relaxed bg-gray-50 p-4 rounded-lg border border-gray-100">
                  {plant.description}
                </p>
              </div>
            )}

            {plant.detailed_description && (
              <div className="mb-8">
                <h2 className="text-xl font-semibold text-gray-900 mb-3 flex items-center">
                  <span className="mr-2">📚</span>
                  详细描述
                </h2>
                <p className="text-gray-700 leading-relaxed">
                  {plant.detailed_description}
                </p>
              </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
              <div className="bg-primary-50 p-4 rounded-lg border border-primary-100">
                <h3 className="text-sm font-medium text-primary-800 mb-3">
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

              {plant.iucn_status && (
                <div className="bg-amber-50 p-4 rounded-lg border border-amber-100">
                  <h3 className="text-sm font-medium text-amber-800 mb-3">
                    🔬 IUCN保护等级
                  </h3>
                  <p className="text-gray-700 font-medium">{plant.iucn_status}</p>
                </div>
              )}

              {plant.uses && plant.uses.length > 0 && (
                <div className="bg-purple-50 p-4 rounded-lg border border-purple-100">
                  <h3 className="text-sm font-medium text-purple-800 mb-3">
                    🔧 主要用途
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {plant.uses.map((use, index) => (
                      <span key={index} className="text-xs px-2 py-1 bg-white text-purple-700 rounded border border-purple-200">
                        {use}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
              {plant.morphology && (
                <div className="bg-green-50 p-4 rounded-lg border border-green-100">
                  <h3 className="text-sm font-medium text-green-800 mb-3">
                    🌿 形态特征
                  </h3>
                  <p className="text-gray-700 leading-relaxed">{plant.morphology}</p>
                </div>
              )}

              {plant.habitat && (
                <div className="bg-blue-50 p-4 rounded-lg border border-blue-100">
                  <h3 className="text-sm font-medium text-blue-800 mb-3">
                    🌍 生态习性
                  </h3>
                  <p className="text-gray-700 leading-relaxed">{plant.habitat}</p>
                </div>
              )}

              {plant.distribution && (
                <div className="bg-teal-50 p-4 rounded-lg border border-teal-100">
                  <h3 className="text-sm font-medium text-teal-800 mb-3">
                    🗺️ 地理分布
                  </h3>
                  <p className="text-gray-700 leading-relaxed">{plant.distribution}</p>
                </div>
              )}

              {plant.garden_zones && plant.garden_zones.length > 0 && (
                <div className="bg-orange-50 p-4 rounded-lg border border-orange-100">
                  <h3 className="text-sm font-medium text-orange-800 mb-3">
                    🏛️ 园区分布
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {plant.garden_zones.map((zone, index) => (
                      <Link
                        key={index}
                        to={`/plants?zone=${encodeURIComponent(zone)}`}
                        className="px-3 py-1 bg-white text-orange-700 rounded-full text-sm hover:bg-orange-100 transition-colors border border-orange-200"
                      >
                        {zone}
                      </Link>
                    ))}
                  </div>
                </div>
              )}
            </div>

            <div className="bg-gradient-to-r from-pink-50 via-purple-50 to-pink-50 p-6 rounded-lg border border-pink-100 mb-8">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <span className="mr-2">🌸</span>
                物候期与生长特征
              </h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {plant.flowering_period && (
                  <div className="text-center">
                    <div className="text-3xl mb-2">🌸</div>
                    <div className="text-xs text-gray-500 mb-1">花期</div>
                    <div className="text-sm font-medium text-gray-900">{plant.flowering_period}</div>
                  </div>
                )}
                {plant.fruiting_period && (
                  <div className="text-center">
                    <div className="text-3xl mb-2">🍎</div>
                    <div className="text-xs text-gray-500 mb-1">果期</div>
                    <div className="text-sm font-medium text-gray-900">{plant.fruiting_period}</div>
                  </div>
                )}
                {plant.max_height && (
                  <div className="text-center">
                    <div className="text-3xl mb-2">📏</div>
                    <div className="text-xs text-gray-500 mb-1">最大高度</div>
                    <div className="text-sm font-medium text-gray-900">{plant.max_height}</div>
                  </div>
                )}
                {plant.lifespan && (
                  <div className="text-center">
                    <div className="text-3xl mb-2">⏳</div>
                    <div className="text-xs text-gray-500 mb-1">寿命</div>
                    <div className="text-sm font-medium text-gray-900">{plant.lifespan}</div>
                  </div>
                )}
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
              {plant.light_requirements && (
                <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-100">
                  <h3 className="text-sm font-medium text-yellow-800 mb-3">
                    ☀️ 光照需求
                  </h3>
                  <p className="text-gray-700">{plant.light_requirements}</p>
                </div>
              )}

              {plant.water_requirements && (
                <div className="bg-cyan-50 p-4 rounded-lg border border-cyan-100">
                  <h3 className="text-sm font-medium text-cyan-800 mb-3">
                    💧 水分需求
                  </h3>
                  <p className="text-gray-700">{plant.water_requirements}</p>
                </div>
              )}

              {plant.soil_preference && (
                <div className="bg-amber-50 p-4 rounded-lg border border-amber-100">
                  <h3 className="text-sm font-medium text-amber-800 mb-3">
                    🌱 土壤偏好
                  </h3>
                  <p className="text-gray-700">{plant.soil_preference}</p>
                </div>
              )}

              {plant.growth_rate && (
                <div className="bg-lime-50 p-4 rounded-lg border border-lime-100">
                  <h3 className="text-sm font-medium text-lime-800 mb-3">
                    📈 生长速度
                  </h3>
                  <p className="text-gray-700">{plant.growth_rate}</p>
                </div>
              )}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              {plant.leaf_type && (
                <div className="bg-emerald-50 p-4 rounded-lg border border-emerald-100">
                  <h3 className="text-sm font-medium text-emerald-800 mb-2">
                    🍃 叶型
                  </h3>
                  <p className="text-gray-700">{plant.leaf_type}</p>
                </div>
              )}

              {plant.flower_color && (
                <div className="bg-pink-50 p-4 rounded-lg border border-pink-100">
                  <h3 className="text-sm font-medium text-pink-800 mb-2">
                    🌺 花色
                  </h3>
                  <p className="text-gray-700">{plant.flower_color}</p>
                </div>
              )}

              {plant.fruit_color && (
                <div className="bg-rose-50 p-4 rounded-lg border border-rose-100">
                  <h3 className="text-sm font-medium text-rose-800 mb-2">
                    🍇 果色
                  </h3>
                  <p className="text-gray-700">{plant.fruit_color}</p>
                </div>
              )}
            </div>

            {plant.medicinal_uses && (
              <div className="bg-red-50 p-4 rounded-lg border border-red-100 mb-8">
                <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center">
                  <span className="mr-2">💊</span>
                  药用价值
                </h3>
                <p className="text-gray-700 leading-relaxed">{plant.medicinal_uses}</p>
              </div>
            )}

            {plant.ornamental_value && (
              <div className="bg-violet-50 p-4 rounded-lg border border-violet-100 mb-8">
                <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center">
                  <span className="mr-2">🎨</span>
                  观赏价值
                </h3>
                <p className="text-gray-700 leading-relaxed">{plant.ornamental_value}</p>
              </div>
            )}

            {plant.ecological_value && (
              <div className="bg-green-50 p-4 rounded-lg border border-green-100 mb-8">
                <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center">
                  <span className="mr-2">🌍</span>
                  生态价值
                </h3>
                <p className="text-gray-700 leading-relaxed">{plant.ecological_value}</p>
              </div>
            )}

            {plant.cultural_significance && (
              <div className="bg-indigo-50 p-4 rounded-lg border border-indigo-100 mb-8">
                <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center">
                  <span className="mr-2">📖</span>
                  文化意义
                </h3>
                <p className="text-gray-700 leading-relaxed">{plant.cultural_significance}</p>
              </div>
            )}

            {plant.notes && (
              <div className="bg-gray-50 p-4 rounded-lg border border-gray-100 mb-8">
                <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center">
                  <span className="mr-2">📋</span>
                  备注
                </h3>
                <p className="text-gray-700 leading-relaxed">{plant.notes}</p>
              </div>
            )}

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
