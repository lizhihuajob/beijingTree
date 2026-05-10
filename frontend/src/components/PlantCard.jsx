import { Link } from 'react-router-dom'
import { formatProtectionStatus } from '../utils/plantUtils'

function PlantCard({ plant }) {
  const protection = formatProtectionStatus(plant.protection_status)

  return (
    <Link
      to={`/plants/${plant.id}`}
      className="plant-card block bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-all duration-300 border border-gray-100"
    >
      <div className="h-40 bg-gradient-to-br from-primary-100 to-primary-200 flex items-center justify-center">
        <span className="text-5xl">🌱</span>
      </div>

      <div className="p-4">
        <div className="flex items-start justify-between mb-2">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">
              {plant.name_cn}
            </h3>
            <p className="text-sm text-gray-500 italic">
              {plant.name_latin}
            </p>
          </div>
          {protection && (
            <span className={`protection-badge text-xs px-2 py-1 rounded-full ${protection.color}`}>
              {protection.text}
            </span>
          )}
        </div>

        <div className="space-y-1 text-sm text-gray-600">
          <div className="flex items-center">
            <span className="text-primary-600 font-medium">科：</span>
            <span className="ml-1">{plant.family}</span>
          </div>
          <div className="flex items-center">
            <span className="text-primary-600 font-medium">属：</span>
            <span className="ml-1">{plant.genus}</span>
          </div>
        </div>

        <p className="mt-3 text-sm text-gray-500 line-clamp-2">
          {plant.description}
        </p>

        {plant.garden_zones && plant.garden_zones.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-1">
            {plant.garden_zones.slice(0, 2).map((zone, index) => (
              <span
                key={index}
                className="text-xs px-2 py-1 bg-primary-50 text-primary-700 rounded"
              >
                {zone}
              </span>
            ))}
            {plant.garden_zones.length > 2 && (
              <span className="text-xs px-2 py-1 bg-gray-100 text-gray-600 rounded">
                +{plant.garden_zones.length - 2}
              </span>
            )}
          </div>
        )}
      </div>
    </Link>
  )
}

export default PlantCard
