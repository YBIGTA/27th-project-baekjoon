from app.api.api_schema import SolveRequest, SolveResponse


class AISolveService:
    """Service that would call an LLM/agent to produce solution code.

    For now, this is a stub that returns a simple template matching the
    requested language. Replace with real LLM logic later.
    """

    def solve(self, req: SolveRequest) -> SolveResponse:
        lang = req.language
        code = self._bootstrap_code(lang, req.problem)
        return SolveResponse(code=code, language=lang, message="generated")

    def _bootstrap_code(self, lang: str, problem: str) -> str:
        if lang == "python":
            return """# Auto-generated solution stub
import sys

def solve():
    data = sys.stdin.read().strip().split()
    # TODO: implement based on problem description
    print(0)

if __name__ == '__main__':
    solve()
"""
        if lang == "cpp":
            return """// Auto-generated solution stub
#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    // TODO: implement based on problem description
    cout << 0 << "\n";
    return 0;
}
"""
        if lang == "java":
            return """// Auto-generated solution stub
import java.io.*;
import java.util.*;
public class Main {
  public static void main(String[] args) throws Exception {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    // TODO: implement based on problem description
    System.out.println(0);
  }
}
"""
        if lang == "js":
            return r"""// Auto-generated solution stub
const fs = require('fs');
const input = fs.readFileSync(0, 'utf8').trim().split(/\s+/);
// TODO: implement based on problem description
console.log(0);
"""
        return "// unsupported language"
