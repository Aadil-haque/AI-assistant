import "./layout.css";
export default function MainLayout({ sidebar, children }) {
    return (
        <main className="main-layout">

            {sidebar}

            <section className="chat-layout">
                {children}
            </section>

        </main>
    );
}