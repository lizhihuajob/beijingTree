import { Link } from 'react-router-dom'
import { formatProtectionStatus } from '../utils/plantUtils'

function PlantCard({ plant }) {
  const protection = formatProtectionStatus(plant.protection_status)
  const hasImage = plant.primary_image && plant.primary_image.length > 0

  return (
    <Link
      to={`/plants/${plant.id}`}
      className="plant-card block bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-all duration-300 border border-gray-100 hover:-translate-y-1"
    >
      <div className="relative h-48 bg-gradient-to-br from-primary-100 to-primary-200 overflow-hidden">
        {hasImage ? (
          <img
            src={plant.primary_image}
            alt={plant.name_cn}
            className="w-full h-full object-cover transition-transform duration-300 hover:scale-105"
            onError={(e) => {
              e.target.style.display = 'none'
              e.target.nextSibling.style.display = 'flex'
            }}
          />
        ) : null}
        <div className={`${hasImage ? 'hidden' : 'flex'} w-full h-full items-center justify-center`}>
          <span className="text-5xl">🌱</span>
        </div>
        
        {protection && (
          <span className={`absolute top-3 right-3 protection-badge text-xs px-2 py-1 rounded-full shadow-sm ${protection.color}`}>
            {protection.text}
          </span>
        )}
      </div>

      <div className="p-4">
        <div className="flex items-start justify-between mb-2">
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-900 truncate">
              {plant.name_cn}
            </h3>
            <p className="text-sm text-gray-500 italic truncate">
              {plant.name_latin}
            </p>
          </div>
        </div>

        <div className="space-y-1 text-sm text-gray-600">
          <div className="flex items-center">
            <span className="text-primary-600 font-medium">科：</span>
            <span className="ml-1 truncate">{plant.family}</span>
          </div>
          <div className="flex items-center">
            <span className="text-primary-600 font-medium">属：</span>
            <span className="ml-1 truncate">{plant.genus}</span>
          </div>
        </div>

        <p className="mt-3 text-sm text-gray-500 line-clamp-2 h-10 overflow-hidden">
          {plant.description}
        </p>

        <div className="mt-3 flex flex-wrap gap-2">
          {plant.flowering_period && (
            <span className="text-xs px-2 py-1 bg-pink-50 text-pink-700 rounded flex items-center">
              <span className="mr-1">🌸</span>{plant.flowering_period}
            </span>
          )}
          {plant.flower_color && (
            <span className="text-xs px-2 py-1 bg-purple-50 text-purple-700 rounded flex items-center">
              <span className="mr-1">🎨</span>{plant.flower_color}
            </span>
          )}
        </div>

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
