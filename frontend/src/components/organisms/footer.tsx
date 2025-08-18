export default function Footer() {
  return (
    <footer className="w-full bg-muted border-t border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
          <p className="text-sm text-muted-foreground">© 2025 BaekjoonHelper. 모든 권리 보유.</p>
          <div className="flex gap-6 text-sm text-muted-foreground">
            <a href="#" className="hover:text-primary transition-colors">
              개인정보처리방침
            </a>
            <a href="#" className="hover:text-primary transition-colors">
              이용약관
            </a>
            <a href="#" className="hover:text-primary transition-colors">
              고객지원
            </a>
          </div>
        </div>
      </div>
    </footer>
  )
}
