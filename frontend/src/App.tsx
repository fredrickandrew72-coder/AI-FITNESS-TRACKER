import './App.css'
import { useEffect, useState } from 'react'

type DetectionResult = {
  detected: boolean
  food_name?: string
  confidence?: number
  requires_clarification?: boolean
  message?: string
  options?: string[]
}

type FoodLog = {
  log_id: string
  food_id: string
  quantity_g: number
  meal_type: string | null
  input_method: string
  logged_at: string
}

type LoggedNutrition = {
  logged_at?: string
  log_id: string
  food_name: string
  quantity_g: number
  energy_kcal?: number | null
  protein_g?: number | null
  carbohydrate_g?: number | null
  fat_g?: number | null
  fiber_g?: number | null
  source: string
}

type NutritionTotals = {
  calories: number
  protein: number
  carbohydrates: number
  fat: number
}

type NutritionResult = {
  food_id?: string
  food_name?: string
  energy_kcal?: number
  protein_g?: number
  carbohydrate_g?: number
  fat_g?: number
  fiber_g?: number
  serving_unit?: string
  serving_energy_kcal?: number
  serving_protein_g?: number
  serving_carbohydrate_g?: number
  serving_fat_g?: number
  serving_fiber_g?: number
  [key: string]: unknown
}

function App() {
  const [selectedImage, setSelectedImage] = useState<File | null>(null)
  const [detection, setDetection] = useState<DetectionResult | null>(null)
  const [selectedFoodType, setSelectedFoodType] = useState('')
  const [nutrition, setNutrition] = useState<NutritionResult | null>(null)
  const [message, setMessage] = useState('')
  const [quantity, setQuantity] = useState(1)
  const [recentLogs, setRecentLogs] = useState<LoggedNutrition[]>([])
  const [totals, setTotals] = useState<NutritionTotals>({
    calories: 0,
    protein: 0,
    carbohydrates: 0,
    fat: 0,
  })
  const [dashboardMessage, setDashboardMessage] = useState('')

  const loadDashboard = async () => {
    try {
      setDashboardMessage('Loading nutrition dashboard...')

      const logsResponse = await fetch(
        'http://127.0.0.1:8000/food-logs/643187da-c09a-4465-a604-47b6da126e69'
      )

      if (!logsResponse.ok) {
        setDashboardMessage('Could not load food logs.')
        return
      }

      const logs: FoodLog[] = await logsResponse.json()

      const today = new Date().toLocaleDateString()

      const nutritionResults = await Promise.all(
        logs.map(async (log) => {
          const response = await fetch(
            'http://127.0.0.1:8000/nutrition/food-log/' + log.log_id
          )

          if (!response.ok) {
            return null
          }

          return { ...(await response.json()), logged_at: log.logged_at } as LoggedNutrition
        })
      )

      const validResults = nutritionResults.filter(
        (item): item is LoggedNutrition => item !== null
      )

      setRecentLogs(validResults.slice(0, 10))

      const todayResults = validResults.filter((item) => {
        const matchingLog = logs.find((log) => log.log_id === item.log_id)
        return matchingLog && new Date(matchingLog.logged_at).toLocaleDateString() === today
      })

      setTotals({
        calories: todayResults.reduce((sum, item) => sum + (item.energy_kcal ?? 0), 0),
        protein: todayResults.reduce((sum, item) => sum + (item.protein_g ?? 0), 0),
        carbohydrates: todayResults.reduce((sum, item) => sum + (item.carbohydrate_g ?? 0), 0),
        fat: todayResults.reduce((sum, item) => sum + (item.fat_g ?? 0), 0),
      })

      setDashboardMessage('')
    } catch (error) {
      console.error(error)
      setDashboardMessage('Could not connect to load the nutrition dashboard.')
    }
  }

  useEffect(() => {
    void loadDashboard()
  }, [])

  const handleImageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0] ?? null
    setSelectedImage(file)
    setDetection(null)
    setSelectedFoodType('')
    setNutrition(null)
    setMessage('')
  }

  const detectFood = async () => {
    if (!selectedImage) {
      setMessage('Please select a food image first.')
      return
    }

    setMessage('')

    const formData = new FormData()
    formData.append('file', selectedImage)

    try {
      const response = await fetch('http://127.0.0.1:8000/food-detection/', {
        method: 'POST',
        body: formData,
      })

      const data = await response.json()

      if (!response.ok) {
        setMessage(data.detail ?? 'Detection failed.')
        return
      }

      setDetection(data)
    } catch (error) {
      console.error(error)
      setMessage('Could not connect to the backend.')
    }
  }

  const confirmAndLogFood = async () => {
    if (!nutrition?.food_id) {
      setMessage('Nutrition information is not available.')
      return
    }

    if (!quantity || quantity <= 0) {
      setMessage('Please enter a valid quantity.')
      return
    }

    if (!nutrition.energy_kcal || !nutrition.serving_energy_kcal) {
      setMessage('Serving information is incomplete.')
      return
    }

    const servingWeightG =
      (nutrition.serving_energy_kcal / nutrition.energy_kcal) * 100

    const quantityG = servingWeightG * quantity

    setMessage('Logging food...')

    try {
      const response = await fetch('http://127.0.0.1:8000/food-logs/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: '643187da-c09a-4465-a604-47b6da126e69',
          food_id: nutrition.food_id,
          quantity_g: quantityG,
          meal_type: null,
          input_method: 'image',
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        setMessage(data.detail ?? 'Could not log food.')
        return
      }
      setMessage('Food logged successfully: ' + quantityG.toFixed(2) + ' g of ' + (nutrition.food_name ?? selectedFoodType) + '.')
      await loadDashboard()
    } catch (error) {
      console.error(error)
      setMessage('Could not connect to the backend.')
    }
  }

  const lookupNutrition = async (foodType: string) => {
    setSelectedFoodType(foodType)
    setNutrition(null)
    setMessage('Looking up nutrition...')

    try {
      const foodResponse = await fetch('http://127.0.0.1:8000/foods/search?name=' + encodeURIComponent(foodType))

      if (!foodResponse.ok) {
        setMessage('Could not load food items.')
        return
      }

      const foods = await foodResponse.json()

      const food = foods[0];

      if (!food?.food_id) {
        setMessage('Nutrition record not found for ' + foodType + '.')
        return
      }

      const nutritionResponse = await fetch(
        'http://127.0.0.1:8000/recipe-nutrition/' + food.food_id
      )

      const nutritionData = await nutritionResponse.json()

      if (!nutritionResponse.ok) {
        setMessage(
          nutritionData.detail ?? 'Could not retrieve nutrition information.'
        )
        return
      }

      setNutrition(nutritionData)
      setMessage('')
    } catch (error) {
      console.error(error)
      setMessage('Could not connect to the backend.')
    }
  }

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="brand">
          <div className="brand-mark">AF</div>
          <div>
            <h1>AI Fitness Tracker</h1>
            <p>AI-powered food and nutrition assistant</p>
          </div>
        </div>
        <span className="status-pill">Nutrition assistant</span>
      </header>

      <section className="welcome">
        <span className="eyebrow">YOUR DAILY WELLNESS</span>
        <h2>Eat better. Feel stronger.</h2>
        <p>Track your meals, understand your nutrition, and make every bite count with your AI-powered food assistant.</p>
      </section>

      <main className="dashboard-grid">
        <section className="panel">
          <div className="panel-heading">
            <div>
              <h2>Food Logging</h2>
              <p>Upload a food image to identify it and estimate its nutrition.</p>
            </div>
          </div>

          <input
            type="file"
            accept="image/*"
            onChange={handleImageChange}
          />

          {selectedImage && (
            <p>Selected image: {selectedImage.name}</p>
          )}

          <button onClick={detectFood}>
            Detect Food
          </button>

          {detection && detection.detected && (
            <div>
              <h3>Detection Result</h3>

              <p>
                <strong>Food:</strong> {detection.food_name}
              </p>

              <p>
                <strong>Confidence:</strong>{' '}
                {detection.confidence !== undefined
                  ? ((detection.confidence * 100).toFixed(2) + '%')
                  : 'N/A'}
              </p>

              {detection.requires_clarification && (
                <div>
                  <p>{detection.message}</p>

                  <label>
                    Select Biryani Type:{' '}
                    <select
                      value={selectedFoodType}
                      onChange={(event) =>
                        lookupNutrition(event.target.value)
                      }
                    >
                      <option value="">-- Select --</option>

                      {detection.options?.map((option) => (
                        <option key={option} value={option}>
                          {option}
                        </option>
                      ))}
                    </select>
                  </label>
                </div>
              )}
            </div>
          )}

          {nutrition && (
            <>
            <p><strong>Estimated quantity:</strong> {nutrition.energy_kcal && nutrition.serving_energy_kcal ? ((nutrition.serving_energy_kcal / nutrition.energy_kcal) * 100 * quantity).toFixed(2) : 'N/A'} g</p>
            <div>
              <h3>Quantity</h3>
              <label>
                Servings: {' '}
                <input
                  type="number"
                  min="0.1"
                  step="0.1"
                  value={quantity}
                  onChange={(event) => setQuantity(Number(event.target.value))}
                />
              </label>
            </div>
            <div>
              <h3>Nutrition Information</h3>

              <p>
                <strong>Food:</strong>{' '}
                {nutrition.food_name ?? selectedFoodType}
              </p>

              <p>
                <strong>Calories:</strong>{' '}
                {nutrition.serving_energy_kcal !== undefined ? (nutrition.serving_energy_kcal * quantity).toFixed(2) : 'N/A'}
              </p>

              <p>
                <strong>Protein:</strong>{' '}
                {nutrition.serving_protein_g !== undefined ? (nutrition.serving_protein_g * quantity).toFixed(2) : 'N/A'} g
              </p>

              <p>
                <strong>Carbohydrates:</strong>{' '}
                {nutrition.serving_carbohydrate_g !== undefined ? (nutrition.serving_carbohydrate_g * quantity).toFixed(2) : 'N/A'} g
              </p>

              <p>
                <strong>Fat:</strong>{' '}
                {nutrition.serving_fat_g !== undefined ? (nutrition.serving_fat_g * quantity).toFixed(2) : 'N/A'} g
              </p>
            </div>
            </>
          )}

          {message && <p>{message}</p>}

          {nutrition && (
            <button onClick={confirmAndLogFood}>Confirm & Log Food</button>
          )}

          <button>Log Food Manually</button>
        </section>

        <section>
          <h2>Today's Nutrition</h2>
          <p>Calories: {totals.calories.toFixed(2)} kcal</p>
          <p>Protein: {totals.protein.toFixed(2)} g</p>
          <p>Carbohydrates: {totals.carbohydrates.toFixed(2)} g</p>
          <p>Fat: {totals.fat.toFixed(2)} g</p>
          {dashboardMessage && <p>{dashboardMessage}</p>}
        </section>

        <section>
          <h2>Recent Food Logs</h2>
          {recentLogs.length === 0 ? (
            <p>No food logs recorded today.</p>
          ) : (
            <ul>
              {recentLogs.map((log) => (
                <li key={log.log_id}>
                  <strong>{log.food_name}</strong> - {log.quantity_g.toFixed(2)} g
                  <br />
                  {log.energy_kcal?.toFixed(2) ?? 'N/A'} kcal | Protein: {log.protein_g?.toFixed(2) ?? 'N/A'} g
                  <br />
                  <small>{log.logged_at ? new Date(log.logged_at).toLocaleString() : 'Time unavailable'}</small>
                </li>
              ))}
            </ul>
          )}
        </section>
      </main>
    </div>
  )
}

export default App
