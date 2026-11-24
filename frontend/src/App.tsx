
function App() {
  return (
    <main className="min-h-screen bg-slate-950 text-white">
      {/* Navigation */}
      <header className="border-b border-slate-800">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-blue-600">
              <span className="text-lg">📍</span>
            </div>
            <span className="text-xl font-bold tracking-tight">
              MeetMap
            </span>
          </div>

          <span className="text-sm text-slate-400">
            Plan together, meet anywhere.
          </span>
        </div>
      </header>

      {/* Main content */}
      <section className="mx-auto flex max-w-5xl flex-col items-center px-6 py-24 text-center">
        <span className="mb-5 rounded-full border border-blue-500/30 bg-blue-500/10 px-4 py-2 text-sm text-blue-300">
          A better way to plan meetups
        </span>

        <h1 className="max-w-3xl text-4xl font-bold tracking-tight sm:text-6xl">
          Better meetups start with a{" "}
          <span className="text-blue-400">
            better meeting point.
          </span>
        </h1>

        <p className="mt-6 max-w-2xl text-lg leading-relaxed text-slate-400">
          Bring everyone's locations together and find
          somewhere convenient to meet. Less travelling,
          more time together.
        </p>

        {/* Room actions */}
        <div className="mt-12 grid w-full max-w-2xl gap-5 sm:grid-cols-2">
          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6 text-left">
            <div className="mb-4 text-2xl">✚</div>

            <h2 className="text-lg font-semibold">
              Create a room
            </h2>

            <p className="mt-2 text-sm leading-relaxed text-slate-400">
              Start a new meetup and invite your friends
              to share their locations.
            </p>

            <button
              type="button"
              className="mt-6 w-full rounded-lg bg-blue-600 px-4 py-3 font-medium transition hover:bg-blue-500"
            >
              Create room
            </button>
          </div>

          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6 text-left">
            <div className="mb-4 text-2xl">👥</div>

            <h2 className="text-lg font-semibold">
              Join a room
            </h2>

            <p className="mt-2 text-sm leading-relaxed text-slate-400">
              Already have a room code? Join your group
              and contribute your starting location.
            </p>

            <input
              type="text"
              placeholder="Enter room code"
              className="mt-6 w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-3 text-white outline-none placeholder:text-slate-500 focus:border-blue-500"
            />

            <button
              type="button"
              className="mt-3 w-full rounded-lg border border-slate-700 px-4 py-3 font-medium transition hover:bg-slate-800"
            >
              Join room
            </button>
          </div>
        </div>
      </section>

      <footer className="border-t border-slate-800 py-6 text-center text-sm text-slate-500">
        MeetMap · Find the middle ground.
      </footer>
    </main>
  )
}

export default App
