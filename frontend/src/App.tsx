import './App.css'
import { useEffect, useMemo, useState } from 'react'

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
type NutritionTotals = { calories: number; protein: number; carbohydrates: number; fat: number }
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
type FoodSearchItem = { food_id: string; food_name: string }

const API = 'http://127.0.0.1:8000'
const USER_ID = '643187da-c09a-4465-a604-47b6da126e69'
const emptyTotals: NutritionTotals = { calories: 0, protein: 0, carbohydrates: 0, fat: 0 }

function App() {
  const [selectedImage, setSelectedImage] = useState<File | null>(null)
  const [detection, setDetection] = useState<DetectionResult | null>(null)
  const [selectedFoodType, setSelectedFoodType] = useState('')
  const [nutrition, setNutrition] = useState<NutritionResult | null>(null)
  const [message, setMessage] = useState('')
  const [quantity, setQuantity] = useState(1)
  const [recentLogs, setRecentLogs] = useState<LoggedNutrition[]>([])
  const [totals, setTotals] = useState<NutritionTotals>(emptyTotals)
  const [dashboardMessage, setDashboardMessage] = useState('')
  const [isDetecting, setIsDetecting] = useState(false)
  const [isLogging, setIsLogging] = useState(false)
  const [manualMode, setManualMode] = useState(false)
  const [foodSearch, setFoodSearch] = useState('')
  const [foodOptions, setFoodOptions] = useState<FoodSearchItem[]>([])
  const [manualFoodId, setManualFoodId] = useState('')
  const [manualNutrition, setManualNutrition] = useState<NutritionResult | null>(null)
  const [manualQuantity, setManualQuantity] = useState(1)
  const [isSearching, setIsSearching] = useState(false)

  const todayLabel = useMemo(() => new Date().toLocaleDateString(undefined, {
    weekday: 'long', month: 'long', day: 'numeric',
  }), [])

  const loadDashboard = async () => {
    try {
      setDashboardMessage('Refreshing your nutrition data…')
      const logsResponse = await fetch(`${API}/food-logs/${USER_ID}`)
      if (!logsResponse.ok) {
        setDashboardMessage('Could not load food logs.')
        return
      }
      const logs: FoodLog[] = await logsResponse.json()
      const today = new Date().toLocaleDateString()
      const nutritionResults = await Promise.all(logs.map(async (log) => {
        try {
          const response = await fetch(`${API}/nutrition/food-log/${log.log_id}`)
          if (!response.ok) return null
          return { ...(await response.json()), logged_at: log.logged_at } as LoggedNutrition
        } catch {
          return null
        }
      }))
      const validResults = nutritionResults.filter((item): item is LoggedNutrition => item !== null)
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

  useEffect(() => { void loadDashboard() }, [])

  const handleImageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0] ?? null
    setSelectedImage(file)
    setDetection(null)
    setSelectedFoodType('')
    setNutrition(null)
    setMessage('')
  }

  const lookupNutrition = async (foodType: string) => {
    if (!foodType) return
    setSelectedFoodType(foodType)
    setNutrition(null)
    setMessage('Looking up trusted nutrition data…')
    try {
      const foodNameMapping: Record<string, string> = { 'aloo paratha': 'Potato parantha' }
      const searchName = foodNameMapping[foodType.toLowerCase().trim()] ?? foodType
      const foodResponse = await fetch(`${API}/foods/search?name=${encodeURIComponent(searchName)}`)
      if (!foodResponse.ok) {
        setMessage('Could not load food items.')
        return
      }
      const payload = await foodResponse.json()
      const foods: FoodSearchItem[] = Array.isArray(payload) ? payload : (payload.value ?? [])
      const food = foods[0]
      if (!food?.food_id) {
        setMessage(`Nutrition record not found for ${foodType}. Try manual search.`)
        return
      }
      const nutritionResponse = await fetch(`${API}/recipe-nutrition/${food.food_id}`)
      const nutritionData = await nutritionResponse.json()
      if (!nutritionResponse.ok) {
        setMessage(nutritionData.detail ?? 'Could not retrieve nutrition information.')
        return
      }
      setNutrition(nutritionData)
      setQuantity(1)
      setMessage('')
    } catch (error) {
      console.error(error)
      setMessage('Could not connect to the backend.')
    }
  }

  const detectFood = async () => {
    if (!selectedImage) {
      setMessage('Choose a food photo before starting detection.')
      return
    }
    setMessage('')
    setIsDetecting(true)
    setDetection(null)
    setNutrition(null)
    setSelectedFoodType('')
    const formData = new FormData()
    formData.append('file', selectedImage)
    try {
      const response = await fetch(`${API}/food-detection/`, { method: 'POST', body: formData })
      const data: DetectionResult & { detail?: string } = await response.json()
      if (!response.ok) {
        setMessage(data.detail ?? 'Detection failed.')
        return
      }
      setDetection(data)
      if (!data.detected) {
        setMessage('No food detected. Try a clearer, well-lit image.')
        return
      }
      if (data.requires_clarification) {
        setMessage(data.message ?? 'Choose the correct food type to continue.')
        return
      }
      if (data.food_name) await lookupNutrition(data.food_name)
      else setMessage('Food detected, but the food name is unavailable.')
    } catch (error) {
      console.error(error)
      setMessage('Could not connect to the backend.')
    } finally {
      setIsDetecting(false)
    }
  }

  const servingGrams = (item: NutritionResult | null) => {
    if (!item?.energy_kcal || !item.serving_energy_kcal) return null
    return (item.serving_energy_kcal / item.energy_kcal) * 100
  }

  const logFood = async (item: NutritionResult, servings: number, inputMethod: 'image' | 'manual') => {
    if (!item.food_id) {
      setMessage('Nutrition information is not available.')
      return
    }
    if (!Number.isFinite(servings) || servings <= 0) {
      setMessage('Enter a valid serving quantity.')
      return
    }
    const gramsPerServing = servingGrams(item)
    if (!gramsPerServing) {
      setMessage('Serving information is incomplete.')
      return
    }
    const quantityG = gramsPerServing * servings
    setIsLogging(true)
    setMessage('Saving your food log…')
    try {
      const response = await fetch(`${API}/food-logs/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: USER_ID,
          food_id: item.food_id,
          quantity_g: quantityG,
          meal_type: null,
          input_method: inputMethod,
        }),
      })
      const data = await response.json()
      if (!response.ok) {
        setMessage(data.detail ?? 'Could not log food.')
        return
      }
      setMessage(`${item.food_name ?? 'Food'} logged successfully · ${quantityG.toFixed(0)} g`)
      if (inputMethod === 'manual') {
        setManualNutrition(null)
        setManualFoodId('')
        setFoodSearch('')
        setManualMode(false)
      } else {
        setNutrition(null)
        setDetection(null)
        setSelectedImage(null)
        setSelectedFoodType('')
      }
      await loadDashboard()
    } catch (error) {
      console.error(error)
      setMessage('Could not connect to the backend.')
    } finally {
      setIsLogging(false)
    }
  }

  const searchFoods = async () => {
    if (!foodSearch.trim()) {
      setMessage('Type a food name to search the nutrition database.')
      return
    }
    setIsSearching(true)
    setFoodOptions([])
    setManualNutrition(null)
    setManualFoodId('')
    try {
      const response = await fetch(`${API}/foods/search?name=${encodeURIComponent(foodSearch.trim())}`)
      const payload = await response.json()
      if (!response.ok) {
        setMessage(payload.detail ?? 'Food search failed.')
        return
      }
      const results: FoodSearchItem[] = Array.isArray(payload) ? payload : (payload.value ?? [])
      setFoodOptions(results.slice(0, 12))
      setMessage(results.length ? '' : 'No matching foods found. Try a shorter search term.')
    } catch (error) {
      console.error(error)
      setMessage('Could not connect to the backend.')
    } finally {
      setIsSearching(false)
    }
  }

  const chooseManualFood = async (foodId: string) => {
    setManualFoodId(foodId)
    setManualNutrition(null)
    try {
      const response = await fetch(`${API}/recipe-nutrition/${foodId}`)
      const data = await response.json()
      if (!response.ok) {
        setMessage(data.detail ?? 'Could not retrieve nutrition information.')
        return
      }
      setManualNutrition(data)
      setManualQuantity(1)
      setMessage('')
    } catch (error) {
      console.error(error)
      setMessage('Could not connect to the backend.')
    }
  }

  const activeNutrition = manualMode ? manualNutrition : nutrition
  const activeQuantity = manualMode ? manualQuantity : quantity
  const setActiveQuantity = manualMode ? setManualQuantity : setQuantity


  return (
    <div className="app-shell">
      <aside className="sidebar">
        <a className="brand" href="#overview" aria-label="AI Fitness Tracker home">
          <span className="brand-mark">AF</span>
          <span className="brand-copy"><strong>AI FITNESS TRACKER<span>.</span></strong><small>AI FITNESS TRACKER</small></span>
        </a>
        <div className="nav-label">WORKSPACE</div>
        <nav className="side-nav">
          <a className="nav-link active" href="#overview"><span>◫</span> Overview</a>
          <a className="nav-link" href="#food-logging"><span>⌁</span> Food logging</a>
          <a className="nav-link" href="#nutrition"><span>◉</span> Nutrition</a>
          <a className="nav-link" href="#history"><span>↗</span> Meal history</a>
        </nav>
        <div className="sidebar-bottom">
          <div className="sidebar-tip"><span className="tip-icon">✳</span><strong>Small steps.<br />Stronger habits.</strong><p>Your daily progress starts with one good choice.</p></div>
          <div className="profile"><div className="avatar">A</div><div><strong>Your profile</strong><small>Personal dashboard</small></div><span className="profile-dots">•••</span></div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div className="breadcrumb">Workspace <span>/</span> Overview</div>
          <div className="topbar-right"><span className="live-indicator"><i /> SYSTEM ONLINE</span><div className="top-avatar">A</div></div>
        </header>

        <div className="page-content" id="overview">
          <section className="welcome-row">
            <div><p className="eyebrow">{todayLabel.toUpperCase()}</p><h1>Good food. <em>Great progress.</em></h1><p className="welcome-subtitle">Your nutrition, made clearer. Keep showing up for your goals.</p></div>
            <a className="primary-button quick-action" href="#food-logging"><span>＋</span> Log a meal</a>
          </section>

          <section className="hero-strip">
            <div className="hero-copy"><span className="hero-kicker"><i /> YOUR DAILY SNAPSHOT</span><h2>Build a healthier<br />you, one meal at a time.</h2><p>Track what you eat and understand what your body gets.</p><a href="#nutrition" className="hero-link">View nutrition breakdown <span>↗</span></a></div>
            <div className="hero-art" aria-hidden="true"><div className="orbit orbit-one" /><div className="orbit orbit-two" /><div className="hero-circle"><span>✳</span></div><div className="floating-chip chip-one">✦ &nbsp; Eat mindfully</div><div className="floating-chip chip-two">↗ &nbsp; Stay consistent</div></div>
          </section>

          <section className="section-block" id="nutrition">
            <div className="section-heading"><div><p className="eyebrow">YOUR NUTRITION</p><h2>Today's overview</h2></div><span className="subtle-note">Based on your logged meals</span></div>
            <div className="stats-grid">
              <article className="stat-card calories-card"><div className="stat-top"><span className="stat-icon">◉</span><span className="stat-caption">ENERGY INTAKE</span><span className="stat-more">•••</span></div><strong className="stat-number">{Math.round(totals.calories).toLocaleString()}<small>kcal</small></strong><div className="stat-foot"><span className="stat-dot" /> Calories consumed today</div><div className="stat-line"><i style={{ width: `${Math.min(totals.calories / 2500 * 100, 100)}%` }} /></div></article>
              <article className="stat-card"><div className="stat-top"><span className="stat-icon protein-icon">◆</span><span className="stat-caption">PROTEIN</span></div><strong className="stat-number">{totals.protein.toFixed(1)}<small>g</small></strong><div className="stat-foot">Daily protein intake</div><div className="mini-track"><i className="protein-fill" style={{ width: `${Math.min(totals.protein / 120 * 100, 100)}%` }} /></div></article>
              <article className="stat-card"><div className="stat-top"><span className="stat-icon carbs-icon">▥</span><span className="stat-caption">CARBOHYDRATES</span></div><strong className="stat-number">{totals.carbohydrates.toFixed(1)}<small>g</small></strong><div className="stat-foot">Daily carbohydrate intake</div><div className="mini-track"><i className="carbs-fill" style={{ width: `${Math.min(totals.carbohydrates / 250 * 100, 100)}%` }} /></div></article>
              <article className="stat-card"><div className="stat-top"><span className="stat-icon fat-icon">◌</span><span className="stat-caption">FATS</span></div><strong className="stat-number">{totals.fat.toFixed(1)}<small>g</small></strong><div className="stat-foot">Daily fat intake</div><div className="mini-track"><i className="fat-fill" style={{ width: `${Math.min(totals.fat / 80 * 100, 100)}%` }} /></div></article>
            </div>
          </section>

          <section className="workspace-grid" id="food-logging">
            <article className="surface-card food-card">
              <div className="section-heading card-heading"><div><p className="eyebrow">SMART FOOD JOURNAL</p><h2>Log your food</h2><p className="section-description">Use AI detection or search the nutrition database manually.</p></div><span className="ai-badge">✦ AI POWERED</span></div>
              <div className="mode-tabs"><button className={!manualMode ? 'mode-tab selected' : 'mode-tab'} onClick={() => { setManualMode(false); setMessage('') }}> <span>▧</span> AI food scan</button><button className={manualMode ? 'mode-tab selected' : 'mode-tab'} onClick={() => { setManualMode(true); setMessage('') }}><span>⌕</span> Manual entry</button></div>

              {!manualMode ? <div className="scan-content">
                <label className="upload-zone">
                  <input className="visually-hidden" type="file" accept="image/*" onChange={handleImageChange} />
                  {selectedImage ? <><div className="upload-symbol">✓</div><strong>{selectedImage.name}</strong><span>Photo selected · click to change</span></> : <><div className="upload-symbol">＋</div><strong>Drop your meal photo here</strong><span>or click to browse from your device</span><small>JPG, PNG or WEBP · Clear photos work best</small></>}
                </label>
                <button className="primary-button full-button" onClick={detectFood} disabled={isDetecting || !selectedImage}>{isDetecting ? <><span className="spinner" /> Analysing image…</> : <>✦ &nbsp; Detect food with AI</>}</button>
                {detection?.detected && <div className="detection-panel"><div className="detection-heading"><span className="success-mark">✓</span><div><small>DETECTION RESULT</small><strong>{detection.food_name}</strong></div>{detection.confidence !== undefined && <b>{(detection.confidence * 100).toFixed(1)}%</b>}</div>{detection.requires_clarification && <div className="clarification"><p>{detection.message ?? 'Select the correct biryani type.'}</p><label>Select food type<select value={selectedFoodType} onChange={(event) => lookupNutrition(event.target.value)}><option value="">Choose an option</option>{detection.options?.map((option) => <option key={option} value={option}>{option}</option>)}</select></label></div>}</div>}
              </div> : <div className="manual-content">
                <label className="field-label" htmlFor="food-search">Search food database</label><div className="search-row"><input id="food-search" value={foodSearch} onChange={(event) => setFoodSearch(event.target.value)} onKeyDown={(event) => { if (event.key === 'Enter') void searchFoods() }} placeholder="e.g. Aloo Paratha, Idli, Chicken rice" /><button className="primary-button" onClick={searchFoods} disabled={isSearching}>{isSearching ? 'Searching…' : 'Search'}</button></div>
                {foodOptions.length > 0 && <div className="food-results"><span className="results-label">MATCHING FOODS</span>{foodOptions.map((food) => <button key={food.food_id} className={`food-result ${manualFoodId === food.food_id ? 'chosen' : ''}`} onClick={() => void chooseManualFood(food.food_id)}><span>◈</span>{food.food_name}<b>{manualFoodId === food.food_id ? '✓' : '＋'}</b></button>)}</div>}
              </div>}

              {activeNutrition && <div className="nutrition-preview"><div className="preview-heading"><div><p className="eyebrow">NUTRITION PREVIEW</p><h3>{activeNutrition.food_name ?? selectedFoodType}</h3></div><span className="source-pill">SOURCE · INDB</span></div><div className="serving-row"><span>Serving quantity</span><div className="stepper"><button onClick={() => setActiveQuantity(Math.max(0.1, Number((activeQuantity - 0.5).toFixed(1))))}>−</button><input type="number" min="0.1" step="0.5" value={activeQuantity} onChange={(event) => setActiveQuantity(Number(event.target.value))} /><button onClick={() => setActiveQuantity(Number((activeQuantity + 0.5).toFixed(1)))}>＋</button></div><small>{activeNutrition.serving_unit ?? 'serving'}(s)</small></div><div className="macro-grid"><div><span>Calories</span><strong>{activeNutrition.serving_energy_kcal !== undefined ? (activeNutrition.serving_energy_kcal * activeQuantity).toFixed(0) : '—'}<small>kcal</small></strong></div><div><span>Protein</span><strong>{activeNutrition.serving_protein_g !== undefined ? (activeNutrition.serving_protein_g * activeQuantity).toFixed(1) : '—'}<small>g</small></strong></div><div><span>Carbs</span><strong>{activeNutrition.serving_carbohydrate_g !== undefined ? (activeNutrition.serving_carbohydrate_g * activeQuantity).toFixed(1) : '—'}<small>g</small></strong></div><div><span>Fat</span><strong>{activeNutrition.serving_fat_g !== undefined ? (activeNutrition.serving_fat_g * activeQuantity).toFixed(1) : '—'}<small>g</small></strong></div></div><button className="primary-button full-button log-button" disabled={isLogging} onClick={() => void logFood(activeNutrition, activeQuantity, manualMode ? 'manual' : 'image')}>{isLogging ? 'Saving meal…' : '✓  Confirm & log meal'}</button></div>}
              {message && <p className={`feedback ${message.toLowerCase().includes('successfully') ? 'feedback-success' : ''}`}>{message}</p>}
            </article>

            <aside className="side-stack">
              <article className="surface-card goal-card"><div className="section-heading"><div><p className="eyebrow">DAILY CONSISTENCY</p><h2>Keep your rhythm</h2></div><span className="goal-icon">✳</span></div><div className="goal-visual"><div className="goal-ring"><div><strong>{Math.round(totals.calories).toLocaleString()}</strong><small>KCAL</small></div></div><div className="goal-copy"><strong>Every meal counts.</strong><p>Log your meals to build a clearer picture of your daily nutrition.</p></div></div><a href="#food-logging" className="text-link">Add your next meal <span>→</span></a></article>
              <article className="surface-card source-card"><span className="source-symbol">⌘</span><div><strong>Nutrition you can trust</strong><p>Food values are retrieved from your integrated IFCT / INDB nutrition database.</p></div></article>
            </aside>
          </section>

          <section className="section-block history-section" id="history">
            <div className="section-heading"><div><p className="eyebrow">YOUR FOOD JOURNAL</p><h2>Recent meals</h2></div><button className="quiet-button" onClick={() => void loadDashboard()}>↻ &nbsp; Refresh</button></div>
            {recentLogs.length === 0 ? <div className="empty-state"><span>◷</span><strong>No meals logged yet</strong><p>Your food history will appear here after you log your first meal.</p><a href="#food-logging">Log your first meal →</a></div> : <div className="history-table"><div className="history-header"><span>FOOD</span><span>QUANTITY</span><span>ENERGY</span><span>PROTEIN</span><span>LOGGED</span></div>{recentLogs.map((log) => <div className="history-row" key={log.log_id}><div className="history-food"><span className="meal-icon">◈</span><strong>{log.food_name}</strong></div><span>{log.quantity_g.toFixed(0)} g</span><strong>{log.energy_kcal?.toFixed(0) ?? '—'} kcal</strong><span>{log.protein_g?.toFixed(1) ?? '—'} g</span><time>{log.logged_at ? new Date(log.logged_at).toLocaleString() : '—'}</time></div>)}</div>}
            {dashboardMessage && <p className="dashboard-feedback">{dashboardMessage}</p>}
          </section>
          <footer className="app-footer"><span>FORMA. · AI FITNESS TRACKER</span><span>Eat well. Train smart. Feel good.</span></footer>
        </div>
      </main>
    </div>
  )
}
export default App
