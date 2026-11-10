
import { useState, useEffect } from 'react'
import './App.css'

function getCookie(name) {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) return parts.pop().split(';').shift()
}

function App() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [isSignup, setIsSignup] = useState(false)
  const [email, setEmail] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [authLoading, setAuthLoading] = useState(true)
  const [expression, setExpression] = useState('')
  const [result, setResult] = useState('0')

  useEffect(() => {
    const checkUser = async () => {
      try {
        await fetch('/api/csrf/')

        const response = await fetch('/api/auth/user/')
        const data = await response.json()

        setIsAuthenticated(data.authenticated)

        if (data.authenticated) {
          setUsername(data.username)
        }
      } catch (error) {
        console.error(error)
      } finally {
        setAuthLoading(false)
      }
    }

    checkUser()
  }, [])

  const handleLogin = async (e) => {
    e.preventDefault()

    try {
      const response = await fetch('/api/auth/login/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: username,
          password: password,
        }),
      })

      const data = await response.json()

      if (response.ok) {
        setIsAuthenticated(true)
        setUsername(data.username)
        setPassword('')
      } else {
        alert(data.error)
      }
    } catch (error) {
      console.error(error)
      alert('Something went wrong!')
    }
  }

  const handleSignup = async (e) => {
    e.preventDefault()

    try {
      const response = await fetch('/api/auth/signup/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
          username: username,
          email: email,
          password: password,
          confirm_password: confirmPassword,
        }),
      })

      const data = await response.json()

      if (response.ok) {
        alert(data.message)
        setIsSignup(false)
        setUsername('')
        setEmail('')
        setPassword('')
        setConfirmPassword('')
      } else {
        alert(data.error)
      }
    } catch (error) {
      console.error(error)
      alert('Something went wrong!')
    }
  }

  const handleLogout = async () => {
    try {
      const response = await fetch('/api/auth/logout/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
        },
      })

      const data = await response.json()

      if (response.ok) {
        setIsAuthenticated(false)
        setIsSignup(false)
        setUsername('')
        setPassword('')
        setEmail('')
        setConfirmPassword('')

        alert(data.message)
      }
    } catch (error) {
      console.error(error)
      alert('Logout failed!')
    }
  }

  const handleButtonClick = (value) => {
    if (value === 'C') {
      setExpression('')
      setResult('0')
    } else if (value === 'back') {
      setExpression((previous) => previous.slice(0, -1))
    } else if (value === '=') {
      handleCalculate()
    } else {
      setExpression((previous) => previous + value)
    }
  }


  const handleCalculate = async () => {
    try {
      const response = await fetch('/api/calculator/calculate/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
          expression: expression,
        }),
      })

      const data = await response.json()

      if (response.ok) {
        setResult(String(data.result))
      } else {
        setResult(data.error)
      }
    } catch (error) {
      console.error(error)
      setResult('Something went wrong!')
    }
  }
  return (
    <div className="session-header">
      <h1>Calculator App</h1>

      {authLoading ? (
        <p>Checking login...</p>
      ) : isAuthenticated ? (
        <div className="welcome-text">
          <h2>Welcome, {username}!</h2>
          <div className="calculator">

            <div className="display">
              <p>{expression || '0'}</p>
              <h2>{result}</h2>
            </div>

            <div className="buttons">
              {[
                'C', 'back', '/', '*',
                '7', '8', '9', '-',
                '4', '5', '6', '+',
                '1', '2', '3', '=',
                '0', '.'
              ].map((value) => (
                <button
                  key={value}
                  onClick={() => handleButtonClick(value)}
                >
                  {value === 'back' ? '⌫' : value}
                </button>
              ))}
            </div>

          </div>

          <button className="logout-button" onClick={handleLogout}>
            Logout
          </button>
        </div>
      ) : isSignup ? (
        <>
          <h2>Create Account</h2>

          <form onSubmit={handleSignup}>
            <div>
              <label>Username</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>

            <div>
              <label>Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div>
              <label>Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            <div>
              <label>Confirm Password</label>
              <input
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
              />
            </div>

            <button type="submit">Signup</button>
          </form>

          <p>
            Already have an account?
            <button onClick={() => setIsSignup(false)}>Login</button>
          </p>
        </>
      ) : (
        <>
          <h2>Welcome Back!</h2>

          <form onSubmit={handleLogin}>
            <div>
              <label>Username</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>

            <div>
              <label>Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            <button type="submit">Login</button>
          </form>

          <p>
            Don't have an account?
            <button onClick={() => setIsSignup(true)}>Signup</button>
          </p>
        </>
      )}
    </div>
  )
}

export default App