# 查找 Matt 的 requirements 缺失项

> 现在matt的是不是有两个没有requirements？

<details><summary>2 previous messages</summary>

> 我会核对仓库里 Matt 各个 skill 的文件，看看缺 `requirements` 的是哪几个。
>
> <details><summary>Ran 4 commands</summary>
>
> - Ran `uv run --no-sync python -c "from pathlib import Path; print((Path.home()/'.codex'/'RTK.md').read_text(encoding='utf-8')); print([p.name for p in Path.cwd().iterdir()])"`
> - Ran `uv run --no-cache --no-sync python -c "from pathlib import Path; print((Path.home()/'.codex'/'RTK.md').read_text(encoding='utf-8')); print([p.name for p in Path.cwd().iterdir()])"`
> - Ran `uv run --no-cache --no-sync python -c "from pathlib import Path; import subprocess; print({d:[p.name for p in Path(d).iterdir()] for d in ['working','sources','releases']}); files=subprocess.check_output(['rg','--files','working']).decode('utf-8').splitlines(); print('\n'.join(f for f in files if 'requirement' in f.lower())[:5500]); print('\n'.join(files[:40]))"`
> - Ran `uv run --no-cache --no-sync python -c "from pathlib import Path; root=Path('working/matt'); print([(p.name,[x.name for x in p.iterdir()] if p.is_dir() else None) for p in sorted(root.iterdir())]); print((Path('sources')/'SOURCES_MATT_POCOCK.md').read_text(encoding='utf-8')[:1600])"`
>
> </details>
</details>

是的，`working/matt` 的三个阶段中，第 1 和第 3 阶段缺少 `requirements.md`：

- [1_extract_and_pick](./working/matt/1_extract_and_pick) 已有 `extract.py` 和 `output/`。
- [3_codex_agent_subdir_complement](./working/matt/3_codex_agent_subdir_complement) 目前只有 `.gitkeep`。

第 2 阶段已有 [requirements.md](./working/matt/2_.agent_convention/requirements.md)。

> 第一个阶段，我希望除了所有的正式发布skill外，还额外包括三个in-progress的writing- skills

<details><summary>2 previous messages</summary>

> 我会核对上游的正式发布清单和 `in-progress` 下的 `writing-*` 目录，再把选取规则写进第一阶段的 `requirements.md`，同步更新提取脚本和产物。
>
> <details><summary>Ran 8 commands</summary>
>
> - Ran `@'
> from pathlib import Path
> for name in ('working/matt/1_extract_and_pick/extract.py','working/matt/2_.agent_convention/requirements.md','working/pstack/shared/1_extract_and_pick/requirements.md','sources/SOURCES_MATT_POCOCK.md'):
>  print(name)
>  print(Path(name).read_text(encoding='utf-8'))
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> import subprocess
> up=Path('sources/mattpocock-skills')
> for name in ('working/matt/1_extract_and_pick/output','sources/mattpocock-skills/skills/in-progress','sources/mattpocock-skills','.'):
>  p=Path(name)
>  print(name,sorted(x.name for x in p.iterdir()))
> for p in [up/'.claude-plugin/plugin.json',up/'.agents/install-block.md']:
>  print(p,p.read_text(encoding='utf-8')[:4500])
> print(subprocess.run(['git','status','--short'],capture_output=True,text=True).stdout)
> print(subprocess.run(['rg','--files','--hidden','-g','AGENTS.md','-g','!.git','working','sources'],capture_output=True,text=True).stdout)
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> import runpy, subprocess, json
> stage=Path('working/matt/1_extract_and_pick')
> output=stage/'output'
> env=runpy.run_path(str(stage/'extract.py'))
> state=json.loads((output/env['CACHE_FILE']).read_text())
> tree=env['inventory'](output)
> del tree[env['CACHE_FILE']]
> print('state',state,'actual digest',env['tree_sha256'](tree))
> for args in (['rev-parse','--show-toplevel'],['ls-files','--eol',str(output/'LICENSE'),str(output/'.extract-state.json'),str(stage/'extract.py')],['status','--short','--branch']):
>  r=subprocess.run(['git',*args],capture_output=True,text=True)
>  print(r.returncode,r.stdout,r.stderr)
> up=Path('sources/mattpocock-skills')
> for p in sorted((up/'skills/in-progress').glob('writing-*')): print(p.name,[f.relative_to(p).as_posix() for f in p.rglob('*')])
> print(Path('.gitignore').read_text())
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> import runpy
> stage=Path('working/matt/1_extract_and_pick')
> env=runpy.run_path(str(stage/'extract.py'))
> up=Path('sources/mattpocock-skills').resolve()
> print(env['head_commit'](up))
> print(env['read_release'](up,env['head_commit'](up))[0])
> p=stage/'extract.py'
> b=p.read_bytes()
> print('file line endings',b.count(b'\r\n'),b.count(b'\n'))
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran ````@'
> from pathlib import Path
> stage = Path("working/matt/1_extract_and_pick")
> script = stage / "extract.py"
> source = script.read_text(encoding="utf-8")
> edits = [
>     ("Extract Matt Pocock's published skills", "Extract Matt Pocock's published skills and three in-progress writing skills"),
>     ('CACHE_FILE = Path(".extract-state.json")', '''CACHE_FILE = Path(".extract-state.json")
> IN_PROGRESS_WRITING_SKILLS = ("writing-beats", "writing-fragments", "writing-shape")'''),
>     ('def read_release(', 'def read_selection('),
>     ('''        names.add(name.casefold())
>     return version, skills''', '''        names.add(name.casefold())
>
>     for name in IN_PROGRESS_WRITING_SKILLS:
>         if name.casefold() not in names:
>             skills[name] = PurePosixPath("skills/in-progress") / name
>     return version, skills'''),
>     ('''    current = existing_output(output)''','''    version, skills = read_selection(upstream, commit)
>     selected_paths = sorted(path.as_posix() for path in skills.values())
>     current = existing_output(output)'''),
>     ('''        if previous_commit == commit:''','''        if previous_commit == commit and cache.get("skills") == selected_paths:'''),
>     ('''    version, skills = read_release(upstream, commit)
> ''', ''),
>     ('Output differs from the release.', 'Output differs from the selected skills.'),
>     ('''cache = {"commit": commit, "tree_sha256": tree_sha256(payload)}''', '''cache = {"commit": commit, "skills": selected_paths, "tree_sha256": tree_sha256(payload)}'''),
> ]
> for old, new in edits:
>     assert source.count(old) == 1, old
>     source = source.replace(old, new)
> requirements = stage / "requirements.md"
> assert not requirements.exists()
> requirements.write_text("""# Stage 1 — Extract Matt Pocock skills
>
> Use the checked-out commit of the `sources/mattpocock-skills/` submodule. Include every skill listed in the `skills` array of its `.claude-plugin/plugin.json`. Add these three skills from `skills/in-progress/`:
>
> - `writing-beats`
> - `writing-fragments`
> - `writing-shape`
>
> If the manifest includes one of these three skills, use its published path once. The manifest and these three names define the complete selection.
>
> Copy each selected directory in full to `output/<skill-name>/` and the upstream license to `output/LICENSE`. At v1.3.2 the expected output contains 30 skills (27 published and 3 in progress).
>
> Run the extractor from the repository root.
>
> ```sh
> uv run --locked working/matt/1_extract_and_pick/extract.py
> ```
>
> Reuse a verified snapshot when both the upstream commit and selection match. Refresh a clean snapshot when either changes. Preserve local edits and report an error if a selected skill is missing.
> """, encoding="utf-8", newline="\n")
> script.write_text(source, encoding="utf-8", newline="\n")
> '@ | uv run --no-cache --no-sync python -X utf8 -````
> - Ran `uv run --no-cache --locked working/matt/1_extract_and_pick/extract.py`
> - Ran `uv run --no-cache --locked working/matt/1_extract_and_pick/extract.py`
> - Ran `@'
> import hashlib, json, runpy, subprocess
> from pathlib import Path, PurePosixPath
> stage=Path("working/matt/1_extract_and_pick")
> output=stage/"output"
> up=Path("sources/mattpocock-skills").resolve()
> git=runpy.run_path(str(stage/"extract.py"))["git"]
> commit=git(up,"rev-parse","HEAD").decode().strip()
> manifest=json.loads(git(up,"show",f"{commit}:.claude-plugin/plugin.json"))
> published={PurePosixPath(p) for p in manifest["skills"]}
> extra={PurePosixPath("skills/in-progress")/name for name in ("writing-beats","writing-fragments","writing-shape")}
> selected=published|extra
> assert {p.name for p in output.iterdir() if p.is_dir()}=={p.name for p in selected}
> rows=git(up,"ls-tree","-rz",commit,"--","LICENSE",*sorted(p.as_posix() for p in selected))
> expected={}
> for row in rows.rstrip(b"\0").split(b"\0"):
>     meta,name=row.split(b"\t")
>     p=PurePosixPath(name.decode())
>     rel=PurePosixPath(*p.parts[2:]) if len(p.parts)>1 else p
>     expected[rel.as_posix()]=meta.split()[2].decode()
> actual={}
> for p in output.rglob("*"):
>     if p.is_file() and p!=output/".extract-state.json":
>         b=p.read_bytes()
>         actual[p.relative_to(output).as_posix()]=hashlib.sha1(f"blob {len(b)}\0".encode()+b).hexdigest()
> assert actual==expected
> print(f"{len(published)} published + {len(extra)} in progress, {len(actual)} files match Git blobs at {commit[:12]}")
> print((stage/"requirements.md").read_text(encoding="utf-8").splitlines()[0])
> r=subprocess.run(["git","status","--short","--ignore-submodules","--","working/matt/1_extract_and_pick"],capture_output=True,text=True,check=True)
> print(r.stdout[:1500])
> '@ | uv run --no-cache --no-sync python -X utf8 -`
>
> </details>
</details>

已更新 Matt 第一阶段的 [requirements.md](./working/matt/1_extract_and_pick/requirements.md) 和 [提取脚本](./working/matt/1_extract_and_pick/extract.py)。脚本会纳入上游清单里的全部正式发布 skill，并额外收录 `in-progress` 中的 `writing-beats`、`writing-fragments` 和 `writing-shape`。如果其中某个以后正式发布，脚本会优先使用正式版，只收录一次。

当前 v1.3.2 的[提取产物](./working/matt/1_extract_and_pick/output)共 **30 个 skill**（27 个正式发布，3 个开发中）。已逐文件核对，86 个产物文件均与上游提交一致，重复运行也已确认命中缓存。

> C:/Users/smy/Desktop/agent-workbench/working/pstack/shared/1_extract_and_pick/requirements.md
> 是不是啰嗦了？还是你写的这个没考虑更新版本时的各种conner case？Constrain部分写的有意义吗

<details><summary>2 previous messages</summary>

> 我会对照两份 `requirements.md` 和提取脚本，重点看升级版本、已有输出和本地修改这几种情况，区分哪些约束保护了实际数据，哪些只是重复描述实现。
>
> <details><summary>Ran 3 commands</summary>
>
> - Ran `@'
> from pathlib import Path
> p=Path('working/pstack/shared/1_extract_and_pick')
> for f in [p/'requirements.md',p/'extract.py']:
>  print(f)
>  for n,line in enumerate(f.read_text(encoding='utf-8').splitlines(),1):
>     print(f'{n:3} {line}')
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> p=Path('working/matt/1_extract_and_pick')
> for f in [p/'requirements.md',p/'extract.py']:
>  print(f)
>  for n,line in enumerate(f.read_text(encoding='utf-8').splitlines(),1):
>     print(f'{n:3} {line}')
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> from tempfile import TemporaryDirectory
> import json, runpy, shutil, subprocess
> extract=runpy.run_path("working/matt/1_extract_and_pick/extract.py")["extract"]
> with TemporaryDirectory() as td:
>     base=Path(td).resolve()
>     repo=base/"repo"
>     repo.mkdir()
>     out=base/"output"
>     def git(*args):
>         subprocess.run(["git","-C",str(repo),"-c","user.name=Fixture","-c","user.email=fixture@example.invalid","-c","core.autocrlf=false","-c","commit.gpgsign=false",*args],check=True,capture_output=True)
>     def write(path, data):
>         p=repo/path
>         p.parent.mkdir(parents=True,exist_ok=True)
>         p.write_bytes(data.encode())
>     def manifest(paths):
>         write(".claude-plugin/plugin.json",json.dumps({"version":"1.0.0","skills":paths}))
>     def commit(msg):
>         git("add","-A")
>         git("commit","-m",msg)
>     def contents(path):
>         return {p.relative_to(path).as_posix():p.read_bytes() for p in path.rglob("*") if p.is_file()}
>     def refuses(path):
>         before=contents(path)
>         try:
>             extract(repo,path)
>         except (ValueError,OSError) as exc:
>             assert contents(path)==before
>             print(str(exc).splitlines()[0][:110])
>         else:
>             raise AssertionError("Expected rejection")
>     git("init")
>     write("LICENSE","license\n")
>     manifest(["skills/productivity/old"])
>     write("skills/productivity/old/SKILL.md","old\n")
>     for name in ("writing-fragments","writing-beats","writing-shape"):
>         write("skills/in-progress/"+name+"/SKILL.md",name+"\n")
>     commit("first")
>     print(extract(repo,out).split(": ")[0])
>     legacy=base/"cacheless"
>     shutil.copytree(out,legacy)
>     (legacy/".extract-state.json").unlink()
>     crlf=base/"crlf"
>     shutil.copytree(out,crlf)
>     (crlf/"LICENSE").write_bytes(b"license\r\n")
>     refuses(crlf)
>     write("skills/productivity/new/SKILL.md","new\n")
>     manifest(["skills/productivity/new","skills/productivity/writing-shape"])
>     (repo/"skills/in-progress/writing-shape").rename(repo/"skills/productivity/writing-shape")
>     write("skills/productivity/writing-shape/SKILL.md","promoted\n")
>     commit("second")
>     print(extract(repo,out).split(": ")[0])
>     assert (out/"writing-shape/SKILL.md").read_bytes()==b"promoted\n" and (out/"new").is_dir() and not (out/"old").exists()
>     refuses(legacy)
>     (repo/"skills/in-progress/writing-beats/SKILL.md").unlink()
>     commit("missing required writing skill")
>     refuses(out)
> print("Verified upgrade, promotion, removal, cache loss, CRLF-only changes and preserved output on rejection")
> '@ | uv run --no-cache --no-sync python -X utf8 -`
>
> </details>
</details>

**pstack 的 `Constrain` 有意义，整篇可以压短。我写的 Matt 版则把“干净的旧快照”说得太含糊了。** 两份文档真正需要讲清楚的是同一个判断：升级时，脚本凭什么认定现有 `output/` 可以安全替换？

pstack 最值得保留的是那张状态表。输出已经等于目标就复用，缺失或为空就生成，等于父仓库 `HEAD` 里已提交的旧快照就允许升级，其余情况保留现场并报错。它还明确把 Git 正常的换行转换视为干净检出。后面的 `Done Check` 重复了其中几条，`Proof to Show` 又要求复述执行结果，这两处可以精简。至于“整个子模块有任何未提交改动就停止”，这是 pstack 选择的工作流约束。从指定 Git 提交提取文件，本身并不依赖工作区干净。[pstack 阶段一要求](./working/pstack/shared/1_extract_and_pick/requirements.md:19)

我用临时仓库实际跑了 Matt 的升级场景，结果如下。[Matt 提取脚本](./working/matt/1_extract_and_pick/extract.py:190)

| 场景 | Matt 当前行为 |
|---|---|
| 上游提交变化，版本号没变 | 正常刷新，新增的正式 skill 被纳入，移出清单的普通 skill 从输出移除 |
| 指定的 writing skill 转正 | 改用正式发布路径，只保留一份 |
| 指定的 writing skill 消失，也没转正 | 提取失败，保留上一版输出 |
| 旧输出完整，但 `.extract-state.json` 丢失 | 升级被拒绝，因为脚本无法确认这份旧输出可以覆盖 |
| 文件内容只发生 LF → CRLF 转换 | 也被判为本地修改，拒绝刷新 |

所以我会给 Matt 的 `requirements.md` 补一张短表，明确**以什么为升级基线、缓存丢失怎么办、换行转换算不算修改、失败后保留什么**。这里尤其值得定下来的是 Windows 换行策略：现在一次正常的 Git 检出就可能让后续升级被拒绝。相比之下，临时目录怎么建、哈希怎么算，可以留在脚本里。[Matt 阶段一要求](./working/matt/1_extract_and_pick/requirements.md:19)

> 其实pstack的复杂化了，他就是单纯的extract and pick，不需要维护版本，我git提交这么多次，不就是为了版本吗，这个没啥意义。就是直接更新即可，我觉得不需要特别更新啊。只不过，matt的是直接把skills抽出来，别的不要，而pstack应该只保留agents和skills，别的不需要（对吧，docs是给人看的，其他的也用不到）

<details><summary>4 previous messages</summary>

> 我会先核对 pstack 的 `agents/`、`skills/` 有没有引用其他目录，以及后续阶段实际读取哪些文件，再把两个第一阶段简化成直接重新提取。
>
> <details><summary>Ran 4 commands</summary>
>
> - Ran `@'
> from pathlib import Path
> import subprocess
> for p in ['AGENTS.md','working/pstack/README.md','working/matt/1_extract_and_pick/requirements.md','working/pstack/shared/2_.agent_convention/requirements.md','working/pstack/shared/3_autoPR_local_fallback/requirements.md','working/pstack/forks/generic/4_cursor_replacement_generalization/requirements.md','working/pstack/forks/codex/4_cursor_replacement_generalization/requirements.md']:
>  print(p,Path(p).read_text(encoding='utf-8')[:5200])
> r=subprocess.run(['git','status','--short','--ignore-submodules'],capture_output=True,text=True);print(r.stdout[:5000],r.stderr)
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> import subprocess
> for q in ('working/pstack/shared/1_extract_and_pick','working/pstack/shared/1_extract_and_pick/output','sources/cursor-plugins/harness/pstack/claude-code','sources/cursor-plugins','working/matt/1_extract_and_pick/output'):
>  p=Path(q);print(p,sorted(f.name for f in p.iterdir()))
> for p in Path('working/pstack').rglob('requirements.md'):
>  print(str(p),[x.name for x in p.parent.iterdir()])
> for p in [Path('sources/cursor-plugins/harness/pstack/claude-code')]:
>  print([str(f.relative_to(p)) for f in p.rglob('*') if len(f.relative_to(p).parts)<=2])
>  proc=subprocess.run(['rg','-n','-i','(\.claude-plugin|CLAUDE_PLUGIN_ROOT|plugins?/pstack|(?:scripts|docs|commands|hooks|assets)/|\.mcp\.json|LICENSE|pstack\.md)',str(p/'agents'),str(p/'skills')],capture_output=True,encoding='utf-8')
>  print(proc.stdout[:13000])
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> import subprocess,re,collections
> up=Path('sources/cursor-plugins/harness/pstack/claude-code')
> for name in ['docs/harness/claude-code.md','.claude-plugin/plugin.json']:
>  print(name,(up/name).read_text(encoding='utf-8')[:3000])
> for fname in Path('working').rglob('*.md'):
>  if 'output' in fname.parts or 'requirements' not in fname.name and fname.name!='README.md': continue
>  if 'pstack' not in fname.parts and 'matt' not in fname.parts:continue
>  lines=fname.read_text(encoding='utf-8').splitlines()
>  print(fname, '\n'.join(f'{i} {line}' for i,line in enumerate(lines,1) if any(s in line for s in ('adapter','README','docs/','1_extract','3_autoPR_remove')))[:4000])
> for dr in ['skills','agents']:
>  files=list((up/dr).rglob('*.md'))
>  print(dr,len(list((up/dr).glob('*/SKILL.md'))),len(list((up/dr).glob('*.md'))))
>  print('adapter',len([p for p in files if 'docs/harness/claude-code.md' in p.read_text(encoding='utf-8')]))
>  print('links',collections.Counter(re.findall(r'\]\(((?:\.\./)+(?:docs/[^)#]+|README\.md))', '\n'.join(p.read_text(encoding='utf-8') for p in files))))
> print('source exists',[(str(p),p.exists()) for p in [Path('sources/mattpocock-skills/.claude-plugin/plugin.json')]])
>
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> import subprocess,collections
> from hashlib import sha256
> for p in Path('working').rglob('*.py'):
>  if 'output' not in p.parts:print(p)
> for p in Path('working/pstack/forks').rglob('requirements.md'):
>  print(p.as_posix())
>  for i,l in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
>     if ('README' in l or 'adapter' in l or 'docs/' in l or '3_auto' in l):print(i,l[:450])
> for rel,up in [('working/pstack/shared/1_extract_and_pick/output','sources/cursor-plugins/harness/pstack/claude-code'),('working/matt/1_extract_and_pick/output','sources/mattpocock-skills')]:
>  dst=Path(rel); root=Path(up)
>  roots={p.name:p for p in (root/'skills').glob('*/*')} if 'matt' in up else {p.name:p for p in root.iterdir()}
>  extra=[];modified=[];eol=0
>  for f in dst.rglob('*'):
>     if not f.is_file():continue
>     name,*parts=f.relative_to(dst).parts
>     if name in roots: other=roots[name].joinpath(*parts)
>     elif name in ['LICENSE','.extract-state.json']:continue
>     else:other=Path('missing')
>     if not other.is_file():extra.append(str(f))
>     elif f.read_bytes()!=other.read_bytes():
>         if f.read_bytes().replace(b'\r\n',b'\n')==other.read_bytes().replace(b'\r\n',b'\n'):eol+=1
>         else:modified.append(str(f))
>  print('modified',modified[:10],'extra',extra[:10],'eol',eol)
> for p in [Path('sources/cursor-plugins/harness/pstack/claude-code'),Path('sources/mattpocock-skills/skills')]:
>  print('links',[(str(f),f.is_symlink()) for f in p.rglob('*') if f.is_symlink() or f.is_junction()][:30])
> print(Path('pyproject.toml').read_text())
> '@ | uv run --no-cache --no-sync python -X utf8 -`
>
> </details>
>
> pstack 有 22 个 skill 引用了 `docs/harness/claude-code.md`，`poteto-help` 也会链接 README 和指南。我会让第一阶段原样提取 `agents/` 和 `skills/`，并把后续的平台适配要求改为直接参考上游文档，这样第一阶段仍然只负责选文件。
>
> <details><summary>Ran 8 commands</summary>
>
> - Ran `@'
> from pathlib import Path
> for file in ['working/pstack/shared/3_autoPR_local_fallback/requirements.md','working/pstack/forks/generic/dependencies.md','working/pstack/forks/codex/5_codex_agent_subdir_complement/requirements.md']:
>  p=Path(file); print(p,p.read_text(encoding='utf-8')[:2500])
> print((Path('sources/cursor-plugins/harness/pstack/claude-code')/'skills/reframe/SKILL.md').read_text(encoding='utf-8')[:900])
> print([(str(f),f.read_bytes().count(b'\r\n')) for f in [*Path('working/pstack').rglob('requirements.md'),Path('working/pstack/README.md')]])
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran ````@'
> from pathlib import Path
> from textwrap import dedent
> def write(path, source):
>     Path(path).write_text(dedent(source).lstrip(), encoding="utf-8", newline="\n")
> tools = Path("working/tools/extract_selection.py")
> assert not tools.exists()
> write(tools, '''
>     """Replace a stage's generated output with the selected directories."""
>     
>     from collections.abc import Iterable
>     from pathlib import Path
>     from shutil import copytree, rmtree
>     from tempfile import mkdtemp
>     
>     
>     def extract_directories(stage: Path, sources: Iterable[Path]) -> None:
>         stage = stage.resolve(strict=True)
>         output = stage / "output"
>         if output.resolve() != output:
>             raise ValueError(f"Expected a local output directory: {output}")
>         staging = Path(mkdtemp(prefix=".extract-", dir=stage)).resolve(strict=True)
>         if staging.parent != stage:
>             raise ValueError(f"Unexpected staging directory: {staging}")
>         candidate = staging / "new"
>         previous = staging / "previous"
>         try:
>             candidate.mkdir()
>             for source in sources:
>                 copytree(source, candidate / source.name, symlinks=True)
>             if output.exists():
>                 output.rename(previous)
>             try:
>                 candidate.rename(output)
>             except OSError:
>                 if previous.exists():
>                     previous.rename(output)
>                 raise
>             if previous.exists():
>                 rmtree(previous)
>         finally:
>             if not previous.exists():
>                 rmtree(staging)
> ''')
> write("working/matt/1_extract_and_pick/extract.py", '''
>     """Extract Matt's published skills and the three selected writing skills."""
>
>     import json
>     import sys
>     from pathlib import Path
>
>     STAGE = Path(__file__).resolve().parent
>     WORKING = STAGE.parents[1]
>     sys.path.insert(0, str(WORKING / "tools"))
>     from extract_selection import extract_directories
>
>     WRITING_SKILLS = ("writing-beats", "writing-fragments", "writing-shape")
>
>
>     def main() -> None:
>         upstream = WORKING.parent / "sources" / "mattpocock-skills"
>         skills = upstream / "skills"
>         manifest = json.loads((upstream / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
>         published = [upstream / item for item in manifest["skills"]]
>         if not published:
>             raise ValueError("The published skills list is empty")
>         published_names = {path.name.casefold() for path in published}
>         selected = published + [
>             skills / "in-progress" / name for name in WRITING_SKILLS if name not in published_names
>         ]
>         for path in selected:
>             if not path.resolve().is_relative_to(skills) or not (path / "SKILL.md").is_file():
>                 raise ValueError(f"Invalid skill directory: {path}")
>         if len({path.name.casefold() for path in selected}) != len(selected):
>             raise ValueError("Selected skills have conflicting directory names")
>         extract_directories(STAGE, selected)
>         print(f"Extracted {len(selected)} skills to {STAGE / 'output'}")
>
>
>     if __name__ == "__main__":
>         main()
> ''')
> write("working/pstack/shared/1_extract_and_pick/extract.py", '''
>     """Extract pstack's Claude Code agents and skills."""
>
>     import sys
>     from pathlib import Path
>
>     STAGE = Path(__file__).resolve().parent
>     WORKING = STAGE.parents[2]
>     sys.path.insert(0, str(WORKING / "tools"))
>     from extract_selection import extract_directories
>
>
>     def main() -> None:
>         source = WORKING.parent / "sources/cursor-plugins/harness/pstack/claude-code"
>         extract_directories(STAGE, [source / "agents", source / "skills"])
>         print(f"Extracted agents and skills to {STAGE / 'output'}")
>
>
>     if __name__ == "__main__":
>         main()
> ''')
> write("working/pstack/shared/1_extract_and_pick/requirements.md", '''
>     # Stage 1 — Extract pstack agents and skills
>
>     Replace `output/` with the complete `agents/` and `skills/` directories from the local `sources/cursor-plugins/harness/pstack/claude-code/` checkout. Preserve their names, contents, and layout.
>
>     Run from the repository root.
>
>     ```sh
>     uv run --locked working/pstack/shared/1_extract_and_pick/extract.py
>     ```
> ''')
> write("working/matt/1_extract_and_pick/requirements.md", '''
>     # Stage 1 — Extract Matt Pocock skills
>
>     From the local `sources/mattpocock-skills/` checkout, select every skill listed in `.claude-plugin/plugin.json` and three from `skills/in-progress/`: `writing-beats`, `writing-fragments`, and `writing-shape`. If a writing skill has been published, use its manifest path once.
>
>     Replace `output/` with the complete selected directories, each at `output/<skill-name>/`.
>
>     Run from the repository root.
>
>     ```sh
>     uv run --locked working/matt/1_extract_and_pick/extract.py
>     ```
> ''')
> '@ | uv run --no-cache --no-sync python -X utf8 -````
> - Ran `@'
> from pathlib import Path
> import os
> p=Path('sources/cursor-plugins/harness/pstack/claude-code')
> for f in (p/'skills').rglob('*.md'):
>  lines=[line for line in f.read_text(encoding='utf-8').splitlines() if ('docs/guide' in line or 'README.md' in line or 'docs/harness' in line) and 'In Claude Code, read' not in line]
>  if lines: print(f.relative_to(p),*[l[:270] for l in lines],sep='\n')
> for f in [Path('working/pstack/shared/2_.agent_convention'),Path('working/pstack/forks/generic/4_cursor_replacement_generalization')]:
>  print(os.path.relpath(p,f))
>
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran ``@'
> from pathlib import Path
> import os
> up=Path('sources/cursor-plugins/harness/pstack/claude-code')
> pstack=Path('working/pstack')
> files=[pstack/'README.md',*pstack.rglob('requirements.md'),Path('working/matt/2_.agent_convention/requirements.md')]
> for p in files:
>     original=p.read_text(encoding='utf-8')
>     new=original.replace('1_extract/', '1_extract_and_pick/').replace('3_autoPR_remove/', '3_autoPR_local_fallback/')
>     reference=Path(os.path.relpath(up,p.parent)).as_posix()
>     new=new.replace('../1_extract_and_pick/output/docs/guide/07-overnight.md',f'{reference}/docs/guide/07-overnight.md')
>     new=new.replace('../../../shared/1_extract_and_pick/output/docs/harness/claude-code.md',f'{reference}/docs/harness/claude-code.md')
>     new=new.replace('../../../shared/1_extract_and_pick/output/README.md',f'{reference}/README.md')
>     new=new.replace('Use the Claude Code adapter as a reference when revising the original text, then remove the adapter from the output.', 'Use the upstream adapter to translate tool and agent instructions, then remove directions to read that adapter. In `poteto-help`, point README and guide links to the corresponding upstream pages.')
>     new=new.replace(' and the playbook table in `README.md`','')
>     new=new.replace('提取上游快照','提取 agents 和 skills')
>     if new!=original:
>         p.write_text(new,encoding='utf-8',newline='\n')
>         print(p)
> '@ | uv run --no-cache --no-sync python -X utf8 -``
> - Ran `uv run --no-cache --locked python -B working/matt/1_extract_and_pick/extract.py`
> - Ran `uv run --no-cache --locked python -B working/pstack/shared/1_extract_and_pick/extract.py`
> - Ran `@'
> from pathlib import Path
> from tempfile import TemporaryDirectory
> import runpy
> mod=runpy.run_path('working/tools/extract_selection.py')
> extract=mod['extract_directories']
> with TemporaryDirectory() as tmp:
>     root=Path(tmp).resolve()
>     stage=root/'stage'
>     stage.mkdir()
>     src=root/'sources'
>     src.mkdir()
>     for name in ['a','b']:
>         d=src/name
>         d.mkdir()
>         (d/'SKILL.md').write_text(name)
>     extract(stage,[src/'a',src/'b'])
>     out=stage/'output'
>     (out/'stale').touch()
>     (out/'a/SKILL.md').write_text('local')
>     (src/'a/SKILL.md').write_text('new')
>     extract(stage,[src/'a'])
>     assert [p.name for p in out.iterdir()]==['a'] and (out/'a/SKILL.md').read_text()=='new'
>     try:extract(stage,[src/'a',src/'missing'])
>     except FileNotFoundError:pass
>     else:raise AssertionError('missing input accepted')
>     assert [p.name for p in out.iterdir()]==['a'] and (out/'a/SKILL.md').read_text()=='new'
>     assert list(stage.iterdir())==[out]
>     print('Verified direct overwrite, stale removal and copy failure in temporary fixture')
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> from hashlib import sha256
> import re,json
> def tree(d):
>     return {f.relative_to(d).as_posix(): (sha256(f.read_bytes()).digest() if f.is_file() else None) for f in d.rglob('*')}
> ps=Path('working/pstack/shared/1_extract_and_pick/output')
> up=Path('sources/cursor-plugins/harness/pstack/claude-code')
> assert {p.name for p in ps.iterdir()}=={'agents','skills'}
> for name in ('agents','skills'):
>     assert tree(up/name)==tree(ps/name)
> print(f'pstack: {len(list((ps/"agents").glob("*.md")))} agents, {len(list((ps/"skills").glob("*/SKILL.md")))} skills, exact tree and file contents')
> up=Path('sources/mattpocock-skills')
> ma=Path('working/matt/1_extract_and_pick/output')
> paths={p.name:p for p in [up/s for s in json.loads((up/'.claude-plugin/plugin.json').read_text(encoding='utf-8'))['skills']]}
> for name in ('writing-beats','writing-fragments','writing-shape'):
>     paths.setdefault(name,up/'skills/in-progress'/name)
> assert {p.name for p in ma.iterdir()}==set(paths)
> for name,p in paths.items():
>     assert tree(p)==tree(ma/name)
> print(f'matt: {len(paths)} complete skill directories, exact tree and file contents')
> for doc in [*Path('working/pstack').rglob('requirements.md'),Path('working/pstack/README.md'),Path('working/matt/2_.agent_convention/requirements.md')]:
>     for url in re.findall(r'\]\(([^()\s]+)\)',doc.read_text(encoding='utf-8')):
>         if url.startswith(('../','shared/','forks/')):
>             assert (doc.parent/url).exists(), (doc,url)
> print('Verified local spec links')
> '@ | uv run --no-cache --no-sync python -X utf8 -`
>
> </details>
</details>

已把两个第一阶段改成直接提取。每次运行都从本地 `sources/` 重新生成 `output/`，旧文件随之清掉。版本历史交给 Git，脚本里的提交比对和缓存已移除。

| 来源 | 第一阶段保留的内容 | 当前产物 |
|---|---|---|
| [Matt](./working/matt/1_extract_and_pick/requirements.md) | 全部正式发布 skill，加上 `writing-beats`、`writing-fragments`、`writing-shape` | 30 个 skill 目录 |
| [pstack](./working/pstack/shared/1_extract_and_pick/requirements.md) | 完整的 `agents/` 和 `skills/`，包括 skill 自带的脚本和参考资料 | 2 个 agent，59 个 skill |

`docs/` 有一个值得区分的地方：22 个 pstack skill 明确要求 Claude Code 读取其中的适配说明，`poteto-help` 也引用了 README 和指南。第一阶段按你的要求只做原样提取。我已更新第四阶段的规格，要求适配时直接参考上游说明，并处理这些链接。[上游适配说明](./sources/cursor-plugins/harness/pstack/claude-code/docs/harness/claude-code.md)

两个提取脚本都已运行，产物的目录结构和文件内容已逐项核对。

> 已经有文件的目录，帮我去掉gitkeep，这个做成脚本吧，挂在git precommit hook上

<details><summary>4 previous messages</summary>

> 我会先检查仓库里的 `.gitkeep` 和现有 Git hook，再写清理脚本、清理当前目录，并验证提交时会自动处理。
>
> <details><summary>Ran 8 commands</summary>
>
> - Ran `@'
> from pathlib import Path
> import subprocess,collections
> def git(*args):
>  return subprocess.check_output(['git',*args]).decode('utf-8').split('\0')
> paths=git('ls-files','--cached','--others','--exclude-standard','-z')
> submodules=[p for p in paths if p.startswith('sources/') and Path(p).is_dir()]
> keeps=[Path(p) for p in paths if p and Path(p).name=='.gitkeep']
> print('submodules',submodules,'markers in index and worktree',len(keeps))
> for k in keeps:
>  if k.exists():
>     siblings=[p.name+('/' if p.is_dir() else '') for p in k.parent.iterdir() if p!=k]
>     print(k.as_posix(),k.stat().st_size,siblings[:12])
>  else:print('already absent',k)
> print('existing config or hook files', [p for p in paths if p and ('hook' in Path(p).name.lower() or 'pre-commit' in p) and 'output' not in Path(p).parts][:60])
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> import subprocess
> from pathlib import Path
> def git(*args):
>  r=subprocess.run(['git',*args],capture_output=True,encoding='utf-8',errors='replace')
>  print(args,r.returncode,r.stdout[:1600],r.stderr[:500])
> for args in [('config','--show-origin','--get-all','core.hooksPath'),('rev-parse','--git-path','hooks'),('rev-parse','--git-dir'),('diff','--cached','--stat','--ignore-submodules'),('ls-files','--stage','--','.gitmodules')]:
>  git(*args)
> for path in ['.git/hooks','.githooks','scripts','working/tools','.git','.git/config']:
>  p=Path(path)
>  print(p,'dir' if p.is_dir() else 'file' if p.is_file() else 'absent',sorted(f.name for f in p.iterdir()) if p.is_dir() else '')
> for path in [Path('.pre-commit-config.yaml'),Path('pyproject.toml'),Path('AGENTS.md')]:
>  if path.is_file(): print(path,path.read_text(encoding='utf-8')[:1500])
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> import subprocess
> for cmd in [('git','--version'),('git','config','--get','core.autocrlf'),('git','config','--get','core.filemode'),('git','ls-files','--deleted','--','*.gitkeep'),('git','ls-files','--others','--exclude-standard','--','*.gitkeep')]:
>  r=subprocess.run(cmd,capture_output=True,text=True);print(cmd,r.stdout[:700],r.stderr[:300])
> from pathlib import Path
> print('attrs',Path('.gitattributes').exists())
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> hook=Path('.githooks/pre-commit')
> script=Path('working/tools/clean_gitkeeps.py')
> assert not hook.exists() and not script.exists()
> hook.parent.mkdir(exist_ok=True)
> hook.write_text('#!/bin/sh\nexec uv run --no-sync python working/tools/clean_gitkeeps.py --staged\n',encoding='utf-8',newline='\n')
> script.write_text('''"""Remove .gitkeep placeholders from directories Git can retain through other files."""
>
> import argparse
> import os
> import subprocess
> from pathlib import Path
>
> MARKER = ".gitkeep"
>
>
> def git_paths(*args: str) -> set[Path]:
>     output = subprocess.check_output(["git", "ls-files", "-z", *args])
>     return {Path(os.fsdecode(name)) for name in output.split(b"\\0") if name}
>
>
> def redundant_markers(paths: set[Path]) -> set[Path]:
>     markers = {path for path in paths if path.name == MARKER}
>     populated = {
>         parent for path in paths for parent in path.parents
>         if path.name != MARKER or parent != path.parent
>     }
>     return {marker for marker in markers if marker.parent in populated}
>
>
> def main() -> None:
>     parser = argparse.ArgumentParser(description=__doc__)
>     parser.add_argument("--staged", action="store_true", help="also clean the pending commit")
>     args = parser.parse_args()
>
>     root = Path(os.fsdecode(subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).rstrip(b"\\n\\r")))
>     os.chdir(root)
>     indexed = git_paths("--cached")
>     worktree = (indexed - git_paths("--deleted")) | git_paths("--others", "--exclude-standard")
>     remove = redundant_markers(worktree)
>     if args.staged:
>         staged = redundant_markers(indexed)
>         # An unstaged sibling cannot keep this directory in the pending commit.
>         remove -= indexed - staged
>         if staged:
>             paths = b"".join(os.fsencode(path.as_posix()) + b"\\0" for path in sorted(staged))
>             subprocess.run(
>                 ["git", "--literal-pathspecs", "rm", "--cached", "--force", "--quiet",
>                  "--pathspec-from-file=-", "--pathspec-file-nul"],
>                 input=paths, check=True,
>             )
>
>     for path in sorted(remove):
>         if path.parent.resolve() == root / path.parent and (path.is_symlink() or path.is_file()):
>             path.unlink()
>             print(f"Removed {path.as_posix()}")
>
>
> if __name__ == "__main__":
>     main()
> ''',encoding='utf-8',newline='\n')
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> attrs=Path('.gitattributes')
> assert not attrs.exists()
> attrs.write_text('.githooks/* text eol=lf\n', encoding='ascii',newline='\n')
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `uv run --no-cache --no-sync python working/tools/clean_gitkeeps.py`
> - Ran `@'
> import os,shutil,subprocess,tempfile
> from pathlib import Path
> source=Path.cwd()
> with tempfile.TemporaryDirectory() as t:
>     root=Path(t).resolve()
>     env={**os.environ,'UV_NO_CACHE':'1','UV_PYTHON':str((source/'.venv/Scripts/python.exe').resolve())}
>     def git(*args):
>         p=subprocess.run(['git','-c','user.name=Test','-c','user.email=test@localhost','-c','commit.gpgsign=false',*args],cwd=root,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace')
>         if p.returncode: raise RuntimeError((p.args,p.stdout,p.stderr))
>         return p.stdout
>     def file(name,content=''):
>         f=root/name
>         f.parent.mkdir(parents=True,exist_ok=True)
>         f.write_text(content)
>     git('init')
>     for name in ['.githooks/pre-commit','working/tools/clean_gitkeeps.py','.python-version','.gitattributes']:
>         dst=root/name
>         dst.parent.mkdir(exist_ok=True,parents=True)
>         shutil.copy2(source/name,dst)
>     (root/'.githooks/pre-commit').chmod(0o755)
>     git('config','--local','core.hooksPath','.githooks')
>     names=['with spaces [a]','empty','partial','nested','nested/leaf','ignored','orphan']
>     for name in names:file(name+'/.gitkeep')
>     file('.gitignore','*.tmp\n')
>     file('ignored/temp.tmp')
>     file('orphan/old','old')
>     git('add','.')
>     git('commit','-qm','initial')
>     assert 'orphan/.gitkeep' not in git('ls-tree','-r','--name-only','HEAD')
>     file('with spaces [a]/new','staged')
>     file('partial/new','not staged')
>     git('add','--','with spaces [a]/new') if False else git('--literal-pathspecs','add','--','with spaces [a]/new')
>     file('with spaces [a]/new','unstaged edit')
>     file('orphan/.gitkeep')
>     git('rm','-q','orphan/old')
>     git('add','orphan/.gitkeep')
>     git('commit','-qm','exercise hook')
>     files=set(git('ls-tree','-r','--name-only','HEAD').splitlines())
>     assert {n+'/.gitkeep' for n in ['empty','partial','nested/leaf','ignored','orphan']}<=files
>     assert not {'with spaces [a]/.gitkeep','nested/.gitkeep','partial/new','ignored/temp.tmp'} & files
>     assert not (root/'with spaces [a]/.gitkeep').exists()
>     assert (root/'partial/.gitkeep').exists()
>     assert git('show','HEAD:with spaces [a]/new')=='staged'
>     assert (root/'with spaces [a]/new').read_text()=='unstaged edit'
>     print('Two real commits ran the hook. Checked staged files, partial staging, bracketed names, nested directories, ignored files and last-file removal.')
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> import tempfile, subprocess, os, shutil
> source=Path.cwd()
> with tempfile.TemporaryDirectory() as tmp:
>     repo=Path(tmp)
>     env={**os.environ,'UV_NO_CACHE':'1','UV_PYTHON':str(source/'.venv/Scripts/python.exe')}
>     def git(*args):
>         return subprocess.check_output(['git','-c','user.name=Test','-c','user.email=test@localhost','-c','commit.gpgsign=false',*args],cwd=repo,env=env,text=True,encoding='utf-8')
>     def put(path,data=''):
>         f=repo/path
>         f.parent.mkdir(parents=True,exist_ok=True)
>         f.write_text(data)
>     git('init','-q')
>     for name in ['.githooks/pre-commit','working/tools/clean_gitkeeps.py','.python-version','.gitattributes']:
>         p=repo/name
>         p.parent.mkdir(parents=True,exist_ok=True)
>         shutil.copy2(source/name,p)
>     (repo/'.githooks/pre-commit').chmod(0o755)
>     git('config','--local','core.hooksPath','.githooks')
>     for name in ['with spaces [a]','empty','partial','nested','nested/leaf','ignored','orphan']:
>         put(name+'/.gitkeep')
>     put('.gitignore','*.tmp\n')
>     put('ignored/file.tmp')
>     put('orphan/old','old')
>     git('add','.')
>     git('commit','-qm','initial')
>     assert 'orphan/.gitkeep' not in git('ls-tree','-r','--name-only','HEAD')
>     put('with spaces [a]/new','staged')
>     put('partial/new','not staged')
>     git('--literal-pathspecs','add','--','with spaces [a]/new')
>     put('with spaces [a]/new','unstaged edit')
>     put('orphan/.gitkeep')
>     git('rm','-q','orphan/old')
>     git('add','orphan/.gitkeep')
>     git('commit','-qm','exercise hook')
>     files=set(git('ls-tree','-r','--name-only','HEAD').splitlines())
>     assert {n+'/.gitkeep' for n in ['empty','partial','nested/leaf','ignored','orphan']}<=files
>     assert not {'with spaces [a]/.gitkeep','nested/.gitkeep','partial/new','ignored/file.tmp'} & files
>     assert not (repo/'with spaces [a]/.gitkeep').exists()
>     assert (repo/'partial/.gitkeep').exists()
>     assert git('show','HEAD:with spaces [a]/new')=='staged'
>     assert (repo/'with spaces [a]/new').read_text()=='unstaged edit'
>     print('Two test commits passed: partial staging, empty and populated directories, nested markers, ignored files, bracketed paths and last-file removal.')
> '@ | uv run --no-cache --no-sync python -X utf8 -`
>
> </details>
>
> 当前工作区已清理 7 个 `.gitkeep`。我在临时仓库做了两次真实提交，确认 hook 会清理多余的占位文件，也不会把未暂存的文件或修改带进提交。现在启用当前仓库的 hook。
>
> <details><summary>Ran 2 commands</summary>
>
> - Ran `@'
> import subprocess
> def git(*args):
>     subprocess.run(['git',*args],check=True)
> git('add','--','.gitattributes','working/tools/clean_gitkeeps.py')
> git('add','--chmod=+x','--','.githooks/pre-commit')
> git('config','--local','core.hooksPath','.githooks')
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> import subprocess
> def git(*args):
>     return subprocess.check_output(['git',*args]).decode().strip()
> assert git('config','--local','--get','core.hooksPath')=='.githooks'
> assert Path(git('rev-parse','--git-path','hooks/pre-commit')).resolve()==Path('.githooks/pre-commit').resolve()
> print('active hook',git('rev-parse','--git-path','hooks/pre-commit'))
> print('index entry',git('ls-files','--stage','--','.githooks/pre-commit'))
> git('diff','--cached','--check')
> print('staged',git('diff','--cached','--name-only','--ignore-submodules'))
> print('remaining', [p.as_posix() for p in Path('working').rglob('.gitkeep')])
> r=subprocess.run(['uv','run','--no-cache','--no-sync','python','working/tools/clean_gitkeeps.py'],capture_output=True,text=True,check=True)
> assert not r.stdout
> print('cleanup rerun removed zero files')
> '@ | uv run --no-cache --no-sync python -X utf8 -`
>
> </details>
</details>

已删除 **7 个**多余的 `.gitkeep`，保留了 3 个空目录的占位文件。

当前仓库已启用 [pre-commit hook](./.githooks/pre-commit)。提交时，只要暂存内容里有其他文件能保留该目录，hook 就会自动移除对应的 `.gitkeep`。已用两次测试提交验证，部分暂存的修改也会保持原样。

手动清理可运行 `uv run working/tools/clean_gitkeeps.py`。[清理脚本](./working/tools/clean_gitkeeps.py)、hook 和换行配置已暂存。新克隆的仓库需运行一次 `git config core.hooksPath .githooks` 来启用。

> 适配器没给替换规则的
> - /loop：Autonomous run用它等事件或定时唤醒，Autopilot-full用它每小时检查，Shipping用它盯合并队列。适配器写了怎么跳过 Routines，没写这几处 /loop 怎么办。
> - create-skill：Automate me和技能编写 playbook直接调用 Cursor 内建的技能编写工具。适配器有「怎么读 pstack 自带 Skill」的规则，但没规定这个内建工具用什么替。
> - cursor-team-kit：poteto-mode要求提交前用 /deslop、交付 UI 或 CLI 时用 control-ui / control-cli；开 PR playbook也直接依赖 /deslop。这些是外部插件能力，不是 pstack 自带，适配器没给映射。
> 适配器提到了，但只覆盖一部分
> - 云端 worker：Swarm指定远程执行、起始分支，必要时才切本地。适配器用 worktree 保留了隔离，但没保住远程机器；Session pickup里靠云端 URL 接续的路径也不能照搬。
> - 聊天记录与 worktree 清理：适配器给了 Claude 的记录路径，但 worktree-audit.sh仍把 Cursor 的 .cursor/projects/.../agent-transcripts 写死；清理 playbook还需要核对置顶和活跃会话。改 Skill 文案不会让脚本读到 Claude 的记录。
> - Bugbot：Babysit能用普通 GitHub review thread 处理已有评论；但 watch-pr还识别 Bugbot 和 Cursor 的 automation ID。能读评论，不等于把另一个 reviewer 接上就会自动获得同样的识别和计数。
> 已有明确处理的两项：make-bot-ui的 Routines、webhook、凭据卡在 Claude 适配器里明确跳过；开 PR playbook的内建 PR 工具则有 CLI 后备。
>
> # Stage 4 — Generalize platform-specific instructions
> codex的和generic的，我感觉是不是terms整理的有点多（似乎把一些docs/的弄进来了）？我记得claude code会有一个adaptor段指向的一个文件，然后这个文件已经整理好了一个表？不过这个表似乎不全，上面是另一个AI整理的，你可以审查一下，把所有adaptor真正缺的整理出来。
> 另外，我觉得这个实际上要分两步，第一是找出所有的需适配的，放在一个单独的文档，放一个status: ready-for-human，然后人介入修改目标term，以及对于缺失功能的处理办法，status修改为done；第二步是人再次让Agent据此执行修改。因此，这个requirements应该还会指向另一个Agent在第一步生成的文档。
> 不过这又引出一个版本问题，比如人修改为done，然后第三阶段没有修改，又运行一次，那此时不应该再次过一遍，但是如果上游修改了，那就该过了，这个逻辑就比较复杂，你看看有没有什么简洁优雅的办法

<details><summary>4 previous messages</summary>

> 我会把 Claude Code 适配器、实际提取的 `agents/` 和 `skills/`、两个分支的 Stage 4 规格逐项对照。除了核实你列的例子，我也会检查脚本里的平台依赖，再把结果整理成可由人审定、按输入变化复用的文档。
>
> <details><summary>Ran 13 commands</summary>
>
> - Ran `@'
> from pathlib import Path
> import difflib
> fork=Path('working/pstack/forks')
> docs=list(fork.glob('*/4_*/requirements.md'))
> print(docs[0].read_text(encoding='utf-8'))
> print('DIFF', ''.join(difflib.unified_diff(docs[0].read_text(encoding='utf-8').splitlines(True),docs[1].read_text(encoding='utf-8').splitlines(True),n=1))[:11000])
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> up=Path('sources/cursor-plugins/harness/pstack/claude-code')
> print((up/'docs/harness/claude-code.md').read_text(encoding='utf-8'))
> for p in Path('working/pstack').glob('*/*'): print(p)
> for f in (up/'skills').rglob('*'):
>  if f.is_file() and (f.suffix not in {'.md','.json'} or f.suffix=='.json'):
>     print(f.relative_to(up).as_posix())
> print('stage3 output',Path('working/pstack/shared/3_autoPR_local_fallback/output').exists())
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> import re, collections
> root=Path('working/pstack/shared/1_extract_and_pick/output')
> fs=sorted(f for f in root.rglob('*') if f.is_file())
> def lines(f):return f.read_bytes().decode('utf-8','replace').splitlines()
> for d in ['generic','codex']:
>  p=Path('working/pstack/forks')/d/'4_cursor_replacement_generalization/requirements.md'
>  print(d,[l for l in lines(p) if any(s in l for s in ['Remote execution','Local execution','Worker checkout','Checkout isolation','MCP access','Role settings'])])
> slash=collections.defaultdict(set)
> for f in fs:
>  if f.suffix not in ('.md','.ts','.sh'):continue
>  for l in lines(f):
>     for match in re.finditer(r'(?<![a-zA-Z0-9_./:-])/([a-zA-Z][\w-]*)',l):
>         slash[match[1]].add(f.relative_to(root).as_posix())
> print('slash', ' '.join(sorted(slash)))
> print('frontmatter fields')
> keys=collections.Counter()
> for f in root.rglob('*.md'):
>  ls=lines(f)
>  if ls[:1]!=['---'] or '---' not in ls[1:]:continue
>  keys.update(l.split(':')[0] for l in ls[1:ls.index('---',1)] if ':' in l and l[:1]!=' ')
> print(keys)
> print('stage2',Path('working/pstack/shared/2_.agent_convention/output').exists())
> print('input count',len(fs))
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> import re, collections
> root=Path('working/pstack/shared/1_extract_and_pick/output')
> fs=sorted(f for f in root.rglob('*') if f.is_file())
> def lines(f):return f.read_bytes().decode('utf-8','replace').splitlines()
> pat=re.compile(r'(?i)\bcursor\b|\.cursor\b|\bclaude\b|\bcodex\b|\bbugbot\b|subagent_type|agent.transcript|worktree.audit|/loop|/autopilot|/orchestrate|/deslop|/create-skill|control-(?:ui|cli)|Routines?|MCP|SendToUser|AskQuestion|todolist|Plan Mode|Use as Mode|cloud agent')
> for f in fs:
>  ls=lines(f)
>  hits=[(n,l) for n,l in enumerate(ls,1) if pat.search(l) and not l.startswith('In Claude Code, read ')]
>  if not hits:continue
>  counts=collections.Counter(m.group().lower() for _,l in hits for m in pat.finditer(l))
>  print(f.relative_to(root).as_posix(),','.join(f'{t}({n})' for t,n in counts.most_common(12)))
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> import re, collections
> root=Path('working/pstack/shared/1_extract_and_pick/output')
> fs=sorted(f for f in root.rglob('*') if f.is_file())
> def lines(f):return f.read_bytes().decode('utf-8','replace').splitlines()
> for nm in ['skills/poteto-mode/playbooks/'+s+'.md' for s in ['session-pickup','worktree-cleanup','bug-fix','autopilot-full','autonomous-run','shipping','visual-parity','opening-a-pr','authoring-a-skill']]+['skills/swarm/SKILL.md','skills/poteto-mode/references/bugbot-triage.md','skills/poteto-mode/playbooks/babysit.md']:
>  print(nm)
>  for i,l in enumerate(lines(root/nm),1):
>     print(i,l[:890])
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> import re, collections
> root=Path('working/pstack/shared/1_extract_and_pick/output')
> fs=sorted(f for f in root.rglob('*') if f.is_file())
> def lines(f):return f.read_bytes().decode('utf-8','replace').splitlines()
> for nm in ['agents/comment-sicko.md','agents/poteto-agent.md','skills/poteto-mode/SKILL.md','skills/poteto-help/SKILL.md','skills/arena/SKILL.md','skills/automate-me/SKILL.md','skills/reflect/SKILL.md','skills/setup-pstack/SKILL.md','skills/make-bot-ui/SKILL.md']:
>  print(nm)
>  for i,l in enumerate(lines(root/nm),1):
>     if re.search(r'(?i)Cursor|\.claude|plugin|[A-Za-z]+Ques|\brole\b|\bmodel|MCP|\bTask\b|mode |\bslash\b|\broutin|\bloop\b|action|transcript|deslop|detec|spawn|^\w[\w-]*:|placehold|dashboard|/orchestrate',l):print(i,l[:720])
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> import re, collections
> root=Path('working/pstack/shared/1_extract_and_pick/output')
> fs=sorted(f for f in root.rglob('*') if f.is_file())
> def lines(f):return f.read_bytes().decode('utf-8','replace').splitlines()
> for nm in ['skills/poteto-mode/scripts/worktree-audit.sh','skills/poteto-mode/scripts/watch-pr/github.ts','skills/poteto-mode/scripts/watch-pr/policy.ts','skills/poteto-mode/scripts/watch-pr/github.test.ts','skills/poteto-mode/scripts/bootstrap.ts','skills/recall/SKILL.md','skills/show-me-your-work/SKILL.md']:
>  print(nm)
>  for i,l in enumerate(lines(root/nm),1):
>     if re.search(r'(?i)CURSOR|bugbot|reviewautomation|automation|transcript|\bstore\b|system prompt|group|\$HOME|pin(ned)?\b|safe\b|activity|ready|NATIVE|background|speaker|\.jsonl|botLogin|reviewer',l): print(i,l[:320])
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> import re, collections
> root=Path('working/pstack/shared/1_extract_and_pick/output')
> fs=sorted(f for f in root.rglob('*') if f.is_file())
> def lines(f):return f.read_bytes().decode('utf-8','replace').splitlines()
> for nm in ['skills/poteto-mode/SKILL.md','skills/poteto-help/SKILL.md','skills/poteto-mode/playbooks/visual-parity.md','skills/poteto-mode/playbooks/shipping.md','skills/poteto-mode/playbooks/authoring-a-skill.md','agents/poteto-agent.md','agents/comment-sicko.md','skills/interrogate/SKILL.md']:
>  print(nm)
>  for i,l in enumerate(lines(root/nm),1):
>     pat=r'(?i)\b(cursor|mcp|Task|routine|worker|autopilot|builtin|built-in|Agents Window|Plan Mode|store|subagent|model|Codex|/loop|recommend|inherit-parent|slug)\b|install|plugin|^(icon|paths|color|is_background|model|  - ):'
>     m=re.search(pat,l)
>     if m and not l.startswith('In Claude Code, read '): print(i,l[max(0,m.start()-45):m.end()+190])
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> import re, collections
> root=Path('working/pstack/shared/1_extract_and_pick/output')
> fs=sorted(f for f in root.rglob('*') if f.is_file())
> def lines(f):return f.read_bytes().decode('utf-8','replace').splitlines()
> pat=r'(?i)\b(claude code|codex|claude|cursor|grok|gemini|plugin(s)?|plan mode|background agents?|ReadLints|WebFetch|WebSearch|Shell|StrReplace|Terminal|ReadFile|WriteFile|ComputerUse|CreatePlan|TodoWrite|structured (choice|question)|agent store|root.{0,10}store|workspace.{0,10}store|system prompt|sidebar|dashboard|subagent.{0,5}(id|type)|slash menu|API key|agent id|Project worker|/in-cloud|/autopilot|/orchestrate|MCP|imagegen|image tool|message bus|alwaysApply)\b'
> for f in fs:
>  if f.suffix!='.md': continue
>  counts=collections.Counter()
>  for l in lines(f):
>     if l.startswith('In Claude Code, read '):continue
>     counts.update(m[0].lower() for m in re.finditer(pat,l))
>  if counts:print(f.relative_to(root), ' '.join(counts))
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> import re, collections
> root=Path('working/pstack/shared/1_extract_and_pick/output')
> fs=sorted(f for f in root.rglob('*') if f.is_file())
> def lines(f):return f.read_bytes().decode('utf-8','replace').splitlines()
> for pat in (r'(?i)(/in-cloud|/autopilot\b|/orchestrate|claude plugin update|\.claude-plugin/plugin\.json|/visualize|\bpaths:|is_background:|^icon:|^color:|plugin[s]?/cache/|allow_multiple|store.{0,35}system prompt|cloud-agent URL|agent id|/loop|built.in babysit)',r'(?i)(system prompt|root.{0,12}store|workspace store|shared store|persistent store|worker.md|context.window|dashboard|worker group|worker handle|agent header|project worker|same vendor|another vendor|budget.{0,10}token|rules.*mdc|slash menu|mode sticky|Plan Mode)'):
>  print('SCAN')
>  for f in fs:
>     if f.suffix!='.md':continue
>     for i,l in enumerate(lines(f),1):
>         if l.startswith('In Claude Code, read '):continue
>         ms=list(re.finditer(pat,l))
>         if ms: print(str(f.relative_to(root)).replace('skills\\poteto-mode\\playbooks\\','pb/'),i,' | '.join(l[max(0,m.start()-20):m.end()+30] for m in ms)[:220])
>
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> import re, collections
> root=Path('working/pstack/shared/1_extract_and_pick/output')
> fs=sorted(f for f in root.rglob('*') if f.is_file())
> def lines(f):return f.read_bytes().decode('utf-8','replace').splitlines()
> for nm in ['skills/ketchup/SKILL.md','skills/ketchup-video/SKILL.md','skills/poteto-mode/playbooks/visual-parity.md','skills/poteto-mode/playbooks/opening-a-pr.md','skills/poteto-mode/worker.md','agents/poteto-agent.md','skills/architect/SKILL.md','skills/poteto-help/SKILL.md','skills/arena/SKILL.md']:
>  print(nm)
>  for i,l in enumerate(lines(root/nm),1):
>     if nm.endswith('poteto-help/SKILL.md') and not (35<=i<=66 or 110<=i<=121):continue
>     if nm.endswith('arena/SKILL.md') and i not in (19,30):continue
>     if nm.endswith('architect/SKILL.md') and i>23:continue
>     if nm in ['skills/ketchup/SKILL.md','skills/ketchup-video/SKILL.md'] and not re.search(r'(?i)render|\btool\b|image|video|visualize|attach|preview|display|inline|screen|playwright|ffmpeg|chat',l):continue
>     if l:print(i,l[:900])
>
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> import re, collections
> root=Path('working/pstack/shared/1_extract_and_pick/output')
> fs=sorted(f for f in root.rglob('*') if f.is_file())
> def lines(f):return f.read_bytes().decode('utf-8','replace').splitlines()
> for nm in ['skills/poteto-mode/playbooks/opening-a-pr.md','skills/poteto-mode/playbooks/shipping.md','agents/poteto-agent.md','skills/poteto-mode/worker.md','skills/ketchup/SKILL.md','skills/poteto-mode/playbooks/authoring-a-skill.md']:
>  print(nm)
>  for i,l in enumerate(lines(root/nm),1):
>     if nm.endswith('ketchup/SKILL.md') or nm.endswith('worker.md'):
>         if i not in [3,37,43]:continue
>     print(i,l[:450])
> for f in fs:
>  if f.suffix not in ['.md','.sh','.ts']:continue
>  for i,l in enumerate(lines(f),1):
>     if re.search(r'\b(Edit|Write|Read(?= tool)|TaskOutput|WebFetch|WebSearch|ReadLints|StrReplace|ApplyPatch|Shell tool|subagent type|model picker|sandbox mode|skill-creator|agent teams|workbench|Computer Use|skills\.sh|autosuggest|recording tool|slash menu|skill registry|skill catalog|context compaction|checkpoint|enablement|access token|agent store|state store|shared across machines)\b',l,re.I) and any(t in l.lower() for t in ['tool','agent store','shared across machines','slash menu','checkpoint']):
>         if re.search('Cursor|TaskOutput|WebFetch|WebSearch|ReadLints|StrReplace|Shell tool|agent store|shared across machines|checkpoint',l,re.I):print(f.relative_to(root),i,l[:190])
>
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> import re, collections
> root=Path('working/pstack/shared/1_extract_and_pick/output')
> fs=sorted(f for f in root.rglob('*') if f.is_file())
> def lines(f):return f.read_bytes().decode('utf-8','replace').splitlines()
> for nm in ['skills/poteto-mode/scripts/worktree-audit.sh','skills/poteto-mode/playbooks/babysit.md','skills/poteto-mode/playbooks/eval.md','skills/poteto-mode/playbooks/pause-safely.md','skills/poteto-mode/worker.md','skills/poteto-mode/scripts/watch-pr/github.ts']:
>  print(nm)
>  for i,l in enumerate(lines(root/nm),1):
>     if nm.endswith('github.ts') and not 329<=i<=365:continue
>     if nm.endswith('.sh') and not re.search(r'stat |date |ruby|python|slug|transcript|bucket|^#',l):continue
>     if nm.endswith('eval.md') and i!=22:continue
>     print(i,l[:440])
> print('working tree', __import__('subprocess').check_output(['git','status','--short','--ignore-submodules','--','working/pstack/forks','working/pstack/README.md']).decode()[:1400])
>
> '@ | uv run --no-cache --no-sync python -X utf8 -`
>
> </details>
>
> 核对后有两处会直接影响清单：`/loop` 实际出现在五个执行 playbook 中；云端 worker 则已有“工作树隔离、需要远端机器时跳过”的规则，仍缺的是远端 worker 的接续和共享记录。目前还没有第三阶段的 `output/`，所以我会把这次审查标成基于第一阶段的预审，正式输入生成后再核对差异。
>
> <details><summary>Ran 10 commands</summary>
>
> - Ran `@'
> from pathlib import Path
> for name in ['working/pstack/README.md','working/pstack/shared/3_autoPR_local_fallback/requirements.md']:
>  print(Path(name).read_text(encoding='utf-8'))
> import frontmatter
> from collections import Counter
> root=Path('working/pstack/shared/1_extract_and_pick/output')
> for s in ['is_background','disable-model-invocation','color','paths']:
>  print(s,[(p.parent.name,frontmatter.load(p).get(s)) for p in sorted(root.glob('skills/*/SKILL.md')) if s in frontmatter.load(p)][:4])
> print('help additional', (root/'skills/poteto-help/SKILL.md').read_text(encoding='utf-8').splitlines()[26:34])
> for term in ['/in-cloud','/autopilot','claude plugin update pstack','cursor-team-kit','/visualize','SKILL.md first']:
>  files=[f for f in root.rglob('*.md') if term in f.read_text(encoding='utf-8')]
>  print(term,[f.relative_to(root).as_posix() for f in files][:15])
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> from textwrap import dedent
> p=Path('working/pstack/forks/review_input.py')
> assert not p.exists()
> p.write_text(dedent('''
>     """Identify the input to pstack Stage 4 and check whether its review can be applied."""
>
>     import argparse
>     from hashlib import sha256
>     from pathlib import Path
>
>     import frontmatter
>
>
>     FORKS = Path(__file__).resolve().parent
>     SHARED = FORKS.parent / "shared"
>     ADAPTER = FORKS.parents[2] / "sources/cursor-plugins/harness/pstack/claude-code/docs/harness/claude-code.md"
>     REVIEW = FORKS / "adaptation-review.md"
>
>
>     def input_id(tree: Path, adapter: Path, label: str) -> str:
>         files = {"adapter": adapter}
>         for name in ("agents", "skills"):
>             directory = tree / name
>             if not directory.is_dir():
>                 raise FileNotFoundError(f"Missing review input: {directory}")
>             for path in directory.rglob("*"):
>                 if path.is_file():
>                     files[path.relative_to(tree).as_posix()] = path
>         digest = sha256()
>         for name, path in sorted(files.items()):
>             digest.update(name.encode("utf-8") + b"\\0" + sha256(path.read_bytes()).digest())
>         return f"{label}-{digest.hexdigest()}"
>
>
>     def main() -> int:
>         parser = argparse.ArgumentParser(description=__doc__)
>         mode = parser.add_mutually_exclusive_group()
>         mode.add_argument("--preview", action="store_true", help="inspect the Stage 1 selection")
>         mode.add_argument("--check-apply", action="store_true", help="require a current, approved Stage 3 review")
>         args = parser.parse_args()
>         stage = "1_extract_and_pick" if args.preview else "3_autoPR_local_fallback"
>         try:
>             current = input_id(SHARED / stage / "output", ADAPTER, "preview" if args.preview else "stage3")
>         except OSError as error:
>             parser.exit(1, f"{error}\\n")
>         print(current)
>         if args.check_apply:
>             review = frontmatter.load(REVIEW) if REVIEW.exists() else {}
>             if review.get("status") != "done" or review.get("input_id") != current:
>                 parser.exit(1, "Stage 4 needs human approval for this input.\\n")
>         return 0
>
>
>     if __name__ == "__main__":
>         raise SystemExit(main())
> ''').lstrip(),encoding='utf-8',newline='\n')
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `uv run --no-cache --locked working/pstack/forks/review_input.py --preview`
> - Ran `@'
> from pathlib import Path
> root=Path('working/pstack/shared/1_extract_and_pick/output')
> for f in ['skills/poteto-mode/SKILL.md','skills/recall/SKILL.md','agents/poteto-agent.md','skills/poteto-mode/playbooks/eval.md','skills/poteto-mode/playbooks/autopilot-stack.md']:
>  p=root/f
>  for i,l in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
>     if ('compaction' in l or 'resume' in l.lower() or 'first line' in l or 'Budget' in l or 'when the chat' in l or 'worker' in l and 'mode' in l or 'cloud' in l or 'plan mode' in l.lower() or 'store' in l): print(f,i,l[:540])
> p=root/'skills/poteto-mode/SKILL.md'
> for i in (90,92,94,96,98,100,102,104):print(i,p.read_text(encoding='utf-8').splitlines()[i-1][:1000])
>
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran ``@'
> from pathlib import Path
> p=Path('working/pstack/forks/adaptation-review.md')
> assert not p.exists()
> p.write_text("---\nstatus: ready-for-human\ninput_id: preview-aec144bbf1048751b77fe5a60e268eedd526cd110e957ccb4b696de506885011\n---\n\n# pstack 第四阶段适配清单\n\n本次预审使用第一阶段的 2 个 agent、59 个 skill 及其附带文件。第三阶段尚无产物。正式审定时，以第三阶段实际的 `agents/`、`skills/` 更新证据位置，尤其是迁入 `skills/open-a-pr/SKILL.md` 的步骤。[第三阶段要求][stage3]\n\n22 个 skill 的入口指向同一份 [Claude Code 适配器][AD]。其 Tools、Subagent fields、Models、setup-pstack、Paths 和 Cursor-only features 六节是上游依据。以下按需要人作决定的行为合并重复调用。两列均为可编辑草案，“同通用”继承本行 Generic 栏。人在核对正式输入并审定两列后将 `status` 改为 `done`。\n\n## 适配器未给目标规则\n\n| 调用与证据 | Generic 建议 | Codex 建议 |\n| --- | --- | --- |\n| `/loop` 有五种现场。[自主运行][auto]需要事件唤醒和超时心跳，[全自动队列][full]经授权每小时审计，[交付][ship]等 watcher 在指定队列上限返回 `COMPLETE`，[修 bug][bug]和[视觉对齐][visual]迭代到证据满足条件。帮助里的[提示][prompt]和[配方][recipes]也使用它。 | 分别写出唤醒条件、间隔、停止条件。当前任务能持续等待时使用事件监听或定时复查；只有迭代要求时直接循环。无法持续监听就标明监控缺口。 | 使用当前任务可用的等待、轮询及恢复执行能力。保留一小时和队列上限，单次任务的监控随任务结束。 |\n| Cursor 内建 `create-skill`。[Automate me][ask] 创建或更新个人模式，[编写 playbook][author] 还要求校验 frontmatter、引用与结构性用例。 | 调用可用的 skill 编写流程，缺少专用工具时按原步骤直接维护 skill 文件。 | 可用时调用 `skill-creator`，保留原路径选择、确认和验证。 |\n| `cursor-team-kit` 的 `/deslop` 是提交前的 diff 清理；`control-ui` 和 `control-cli` 要在真实界面取证。[模式入口][mode]、[开 PR][open]、[全自动队列][full]、[交付][ship]、[帮助][help]。 | 分开写清“清理本次 diff”和“操作实际 UI／CLI”。验证用已有控制工具或具名驱动，缺少可达表面时报告验证缺口。 | 同通用。`no-comments` 仍是另一个随包 skill，保留其独立步骤。 |\n| `/visualize` 不在选入的 skills 中。[Ketchup][ketchup] 用它展示数字，还要求聊天中内嵌截图或视频；[视频版][video] 要内嵌已检查的成片。 | 使用可用的图表与媒体呈现能力，保留只读约束、真实截图和渲染失败时的原处理。 | 可用时使用会话的图表能力及本地媒体预览。 |\n| `Use as Mode`、Option/Alt+Enter、Plan Mode、内建 babysit、外部 `/orchestrate` 出现在面向用户的 [poteto-help][help]；[模式入口][mode] 明确把 PR 状态交给 Babysit playbook。 | 写出单次调用、持续模式和只规划的差别。沿用每个新任务显式调用的后备。`/orchestrate` 只是指明命令归属，无需引入编排依赖。 | 同通用。保留 pstack 自带的计划和 Babysit playbook 名称。 |\n| `/add-plugin`、Customize 侧栏、Claude marketplace、`/pstack:…` 以及 README／指南的相对链接在 [poteto-help][help]。交付树只有 agents 和 skills；适配器假定指南也已安装。 | 帮助指向本发行版的安装入口；已打包的文件用本地路径，未打包的 README／指南用对应的上游链接。 | 同通用，帮助中的调用示例改为目标会话支持的 skill 调用方式。 |\n| 加载元数据会改变行为。`disable-model-invocation` 控制显式调用，[TS skill][TS] 声明 `paths`，而 [poteto-mode][mode] 的 `icon/color` 只影响展示。[poteto-agent][role] 还声明 `is_background`。 | 明确显式调用、文件匹配及后台执行各自的实现；缺少匹配能力时写明 TS/TSX 适用范围。展示字段可省略。 | 保留 `disable-model-invocation` 供第五阶段生成 `agents/openai.yaml`。分别审定路径触发、角色加载和后台行为。 |\n\n## 适配器给了规则，仍有行为缺口\n\n| 调用与已覆盖部分 | Generic 建议 | Codex 建议 |\n| --- | --- | --- |\n| [Swarm][swarm] 同时要求远端机器、并发后台 worker 及起始分支。[适配器][AD] 已给隔离工作树、指定分支、后台通知以及“需要云机器或仪表盘时跳过”的规则。[接续][pick] 还收 cloud-agent URL；[全自动队列][full] 要求远端所有者能替换、根 agent 的共享记录能跨机器读取、能探测后代并传达停写。 | 使用既有草案的 `remote agent`／`local subagent`。分别说明隔离与执行地点，保留开始分支。为接续指定可取回的分支、记录、worker 标识和停写通道；缺少必要能力时报告具体步骤。 | 既有草案用 `remote worker`／`local worker`。按会话实际提供的远端执行、查询、通知能力处理；工作树只用于 checkout 隔离。 |\n| `resume` 已有“新开 agent 并传旧结果”的翻译；[模式入口][mode] 却只在未提交 checkout 或仍运行的进程必须延续时要求恢复。同一文件和 [worker.md][worker] 要求子代都能读取 kickoff 指定的文件。[两个][role] [角色][comment] 也需要目标端能加载。 | 普通交接用 brief、分支和结果。依赖活动进程时须恢复原 worker 或明确状态损失；给远端的是其 checkout 可解析的 worker 指令路径。 | 使用可用的命名角色和恢复标识。若角色不能注册，把对应角色指令交给 worker 并保留其职责与权限。 |\n| 适配器给了 Claude 项目和子会话记录路径。[Recall][recall]、[Automate me][ask]、[Eval][eval]、[审计日志][log] 需要限定工作区并读取实际工具记录。[worktree-audit.sh][audit] 第 72–74、111–126 行自己拼 Cursor 路径；没有记录时仍可能给出 `safe`。[清理 playbook][cleanup] 另需核对活跃和置顶会话，还点名 Cursor 本地缓存。 | 给脚本传入限定工作区的记录来源。无法判定占用时保留候选，使用 playbook 已有的人工核对；逐项识别目标端可清理的缓存。 | 优先使用有权读取的当前项目会话和活跃／置顶信息；脚本需要文件时显式提供来源。以“找不到记录”和“确有活跃会话”两例验证脚本与文案。 |\n| [Babysit][babysit] 和[分类指南][triage]可按普通 GitHub thread 处理已有评论。适配器还规定没有 Bugbot check／comment 时跳过相应等待。`watch-pr` 另按作者和正文识别 Bugbot，按 `RUN_ID`／`CURSOR_AUTOMATION_ID` 去重计轮，按 check 名判断自动审查是否运行。[识别代码][watch]、[策略][policy]、[测试][tests]。 | 默认保留真实的 Bugbot 协议和测试，普通 reviewer 走普通 thread。若要支持另一 reviewer，须明确身份、轮次键、check 名及对应测试。 | 同通用。是否增加 reviewer 由人决定。 |\n| [模型配置][setup] 已有 Claude 的 model／effort 和规则文件映射。[Arena][arena] 区分 family 与 vendor；[独立审计][log] 和 [poteto-mode][mode] 要求另一供应商。非 Claude 模型回退到父模型后，这个条件可能失效。旧 slug 迁移、预算、席位数和同家族降级也会影响判断。 | 按可用模型配置角色，单独记录 family 与 vendor。无法完成跨供应商核查时按所在步骤的降级规则报告；保留原有门槛和席位数。角色配置沿用待审路径 `~/.agent/pstack-models.md`，同步读写与加载规则。 | 既有术语为 `pstack model settings`。审定可持久读取的实际位置及模型／推理级别来源，落实相同的跨供应商检查。 |\n| [Automate me][ask] `allow_multiple: true` 要求多选。适配器只明确了工具名称和非交互时改用文字提问。 | 保留可一次选多项的语义；目标控件仅支持单选时，允许以文字提交多个选项。 | 同通用，保留原流程的用户确认。 |\n\n## 有上游依据的常规映射\n\n这些项目也进入实际改写，集中确认目标用语即可。每行列出代表性调用点。\n\n| 来源及适用范围 | Generic 建议 | Codex 建议 |\n| --- | --- | --- |\n| `Task/Agent`、`subagent_type`、`generalPurpose`、`poteto-agent`、`comment-sicko`；只读检查、MCP 访问、后台结果、文件指针。[How][how]、[No comments][noc]、[Recall][recall]、[worker 入口][role] | 用 `subagent` 和对应角色名称；在 brief 中明确只读或需要的 MCP 能力、文件、结果返回方式。 | 同通用；仅传目标工具支持的参数。 |\n| `AskQuestion`、待办清单、`Grep/Glob`、读取文件、调用 pstack 自带 skill。适配器给了直接替代或后备。[Automate me][ask]、[Swarm][swarm]、[模式入口][mode] | 使用结构化提问、任务清单、文件或文本搜索；按名称调用已安装 skill，可按入口路径读取。 | 同通用。包内 skill 名称维持原名。 |\n| 项目／用户 skills、规则文件、插件安装与只读缓存。[反思][reflect]、[创建验证 skill][verify]、[Automate me][ask]、[worker 入口][role] | 保留项目优先、用户目录 `~/.agents/skills/` 和编辑缓存前复制的约束。原草案项目指令为 `.agents/AGENTS.md`，需核实目标实际加载位置。 | 同通用；人可在此更正实际加载位置。 |\n| `make-bot-ui` 的 Routines、`update_state`、webhook、凭据卡和依赖产物已有明确的 Claude 跳过及占位规则。[适配器][AD]、[调用][bot] | 如采用跳过规则，指明具体步骤和依赖的 URL／密钥占位；只有真实接口可用时才描述创建与安全交接。 | 同通用。 |\n| 内建 PR 工具已有 forge CLI 后备。`gh pr create` 默认 ready，Origin 用 `--status open`。第三阶段另加无远端时本地合并。[开 PR][open]、[第三阶段要求][stage3] | 采用实际 forge 工具、CLI 和第三阶段本地后备。 | 同通用。 |\n\n## 从旧 Terms 表移出的内容\n\n`/in-cloud`、`/autopilot` 和 `claude plugin update pstack@cursor-plugins` 在本次选入的 Markdown 中没有调用点。`Autopilot-full` 是实际的 playbook，保留其名称。`TodoWrite`、`AskUserQuestion` 和 `isolation: \"worktree\"` 是适配器给 Claude 的译法，作为依据即可。`watch-pr` 的 GraphQL `endCursor` 是分页字段，`statechart` 的 `loop-check` 是源码模块；两者保留原义。[全自动队列][full]、[分页代码][watch]、[适配器][AD]\n\n[AD]: ../../../sources/cursor-plugins/harness/pstack/claude-code/docs/harness/claude-code.md\n[stage3]: ../shared/3_autoPR_local_fallback/requirements.md\n[mode]: ../shared/1_extract_and_pick/output/skills/poteto-mode/SKILL.md\n[worker]: ../shared/1_extract_and_pick/output/skills/poteto-mode/worker.md\n[role]: ../shared/1_extract_and_pick/output/agents/poteto-agent.md\n[comment]: ../shared/1_extract_and_pick/output/agents/comment-sicko.md\n[help]: ../shared/1_extract_and_pick/output/skills/poteto-help/SKILL.md\n[auto]: ../shared/1_extract_and_pick/output/skills/poteto-mode/playbooks/autonomous-run.md\n[full]: ../shared/1_extract_and_pick/output/skills/poteto-mode/playbooks/autopilot-full.md\n[ship]: ../shared/1_extract_and_pick/output/skills/poteto-mode/playbooks/shipping.md\n[bug]: ../shared/1_extract_and_pick/output/skills/poteto-mode/playbooks/bug-fix.md\n[visual]: ../shared/1_extract_and_pick/output/skills/poteto-mode/playbooks/visual-parity.md\n[author]: ../shared/1_extract_and_pick/output/skills/poteto-mode/playbooks/authoring-a-skill.md\n[open]: ../shared/1_extract_and_pick/output/skills/poteto-mode/playbooks/opening-a-pr.md\n[pick]: ../shared/1_extract_and_pick/output/skills/poteto-mode/playbooks/session-pickup.md\n[cleanup]: ../shared/1_extract_and_pick/output/skills/poteto-mode/playbooks/worktree-cleanup.md\n[audit]: ../shared/1_extract_and_pick/output/skills/poteto-mode/scripts/worktree-audit.sh\n[eval]: ../shared/1_extract_and_pick/output/skills/poteto-mode/playbooks/eval.md\n[watch]: ../shared/1_extract_and_pick/output/skills/poteto-mode/scripts/watch-pr/github.ts\n[policy]: ../shared/1_extract_and_pick/output/skills/poteto-mode/scripts/watch-pr/policy.ts\n[tests]: ../shared/1_extract_and_pick/output/skills/poteto-mode/scripts/watch-pr/github.test.ts\n[babysit]: ../shared/1_extract_and_pick/output/skills/poteto-mode/playbooks/babysit.md\n[triage]: ../shared/1_extract_and_pick/output/skills/poteto-mode/references/bugbot-triage.md\n[swarm]: ../shared/1_extract_and_pick/output/skills/swarm/SKILL.md\n[arena]: ../shared/1_extract_and_pick/output/skills/arena/SKILL.md\n[ask]: ../shared/1_extract_and_pick/output/skills/automate-me/SKILL.md\n[setup]: ../shared/1_extract_and_pick/output/skills/setup-pstack/SKILL.md\n[log]: ../shared/1_extract_and_pick/output/skills/show-me-your-work/SKILL.md\n[recall]: ../shared/1_extract_and_pick/output/skills/recall/SKILL.md\n[reflect]: ../shared/1_extract_and_pick/output/skills/reflect/SKILL.md\n[TS]: ../shared/1_extract_and_pick/output/skills/typescript-best-practices/SKILL.md\n[ketchup]: ../shared/1_extract_and_pick/output/skills/ketchup/SKILL.md\n[video]: ../shared/1_extract_and_pick/output/skills/ketchup-video/SKILL.md\n[bot]: ../shared/1_extract_and_pick/output/skills/make-bot-ui/SKILL.md\n[how]: ../shared/1_extract_and_pick/output/skills/how/SKILL.md\n[verify]: ../shared/1_extract_and_pick/output/skills/create-verification-skill/SKILL.md\n[noc]: ../shared/1_extract_and_pick/output/skills/no-comments/SKILL.md\n[prompt]: ../shared/1_extract_and_pick/output/skills/poteto-help/references/prompting.md\n[recipes]: ../shared/1_extract_and_pick/output/skills/poteto-help/references/recipes.md\n",encoding='utf-8',newline='\n')
> '@ | uv run --no-cache --no-sync python -X utf8 -``
> - Ran ``@'
> from pathlib import Path
> p=Path('working/pstack/README.md')
> before=p.read_text(encoding='utf-8')
> assert '## Stage 4' not in before
> p.write_text(before.rstrip()+'\n\n'+"## Stage 4\n\nGeneric 和 Codex 共用一份[适配清单](forks/adaptation-review.md)。每行记录调用位置、Claude 适配器已覆盖的行为，以及两个 fork 各自的目标术语或缺失能力的处理办法。\n\n1. **调查。** 从仓库根目录运行 `uv run --locked working/pstack/forks/review_input.py`，取得当前 `input_id`。逐项核对第三阶段 `output/agents/`、`output/skills/`，包括脚本、模板、元数据、测试和帮助文字。仅将实际命中的平台行为列入清单，链接到可复查的输入位置。上游 [Claude Code 适配器](../../sources/cursor-plugins/harness/pstack/claude-code/docs/harness/claude-code.md) 用于判定已有映射、部分覆盖和缺口。把目标用语、替代方案或跳过条件写成草案，填入 `input_id`，设 `status: ready-for-human`，交人审定。此步只更新清单。\n2. **审定。** 人可编辑任一列，注明保留原接口、使用哪个目标能力、能力缺失时如何处理。两列都确认后，由人把 `status` 改为 `done`。这个状态表示清单已审定。\n3. **执行。** 人随后明确要求执行某个 fork 时，先运行 `uv run --locked working/pstack/forks/review_input.py --check-apply`。通过后，从第三阶段输入重新生成所选 fork 的 `output/`，只应用对应列的决定。同一输入上调整了决定时，再次明确执行即可按新版决定生成。\n\n`input_id` 来自实际输入文件的相对路径、内容以及上游适配器的内容。Git 提交、文件时间和与这三处无关的修改不会触发重审。\n\n| 再次调查时的状态 | 操作 |\n| --- | --- |\n| 编号相同，`ready-for-human` | 返回已有清单，保留人正在编辑的草案。 |\n| 编号相同，`done` | 复用已审定清单，结束调查。 |\n| 编号变化 | 核对输入差异，保留仍适用的人工决定，标出新增、变更、移除的调用和受影响的决定。写入新编号，回到 `ready-for-human`。 |\n| 第三阶段尚无产物 | 可用 `--preview` 预审第一阶段选出的文件。预审编号以 `preview-` 开头，正式编号以 `stage3-` 开头。首次见到正式输入时，核对预审与第三阶段的实际差异。 |\n",encoding='utf-8',newline='\n')
> for fork,source in [["codex","# Stage 4 — Adapt pstack for Codex\n\nFollow the [two-step review and application workflow](../../../README.md#stage-4). During discovery, update the [shared adaptation review](../../adaptation-review.md) with occurrences from Stage 3 and use the [upstream adapter](../../../../../sources/cursor-plugins/harness/pstack/claude-code/docs/harness/claude-code.md) to check existing coverage. Leave the review at `ready-for-human`.\n\nOn a separate request to apply a current `done` review, read `../../../shared/3_autoPR_local_fallback/output/`, apply the **Codex** column, and write the resulting `agents/` and `skills/` to `./output/`.\n\n- Preserve headings, step order, permissions, concurrency, timing, stopping conditions and verification evidence. Keep edits local to the affected instructions.\n- Apply each approved decision to its callers, executable helpers and associated tests. Preserve literal forge interfaces and fixture values wherever they still describe the actual protocol.\n- Remove instructions to load the Claude adapter after incorporating their approved equivalents. Verify local links and links to the upstream guides, including those in `poteto-help`.\n- If execution uncovers a platform dependency without an approved decision, record it in the review, return it to `ready-for-human`, and present it for review before delivering output.\n"],["generic","# Stage 4 — Generalize pstack for other hosts\n\nFollow the [two-step review and application workflow](../../../README.md#stage-4). During discovery, update the [shared adaptation review](../../adaptation-review.md) with occurrences from Stage 3 and use the [upstream adapter](../../../../../sources/cursor-plugins/harness/pstack/claude-code/docs/harness/claude-code.md) to check existing coverage. Leave the review at `ready-for-human`.\n\nOn a separate request to apply a current `done` review, read `../../../shared/3_autoPR_local_fallback/output/`, apply the **Generic** column, and write the resulting `agents/` and `skills/` to `./output/`.\n\n- Preserve headings, step order, permissions, concurrency, timing, stopping conditions and verification evidence. Keep edits local to the affected instructions.\n- Apply each approved decision to its callers, executable helpers and associated tests. Preserve literal forge interfaces and fixture values wherever they still describe the actual protocol.\n- Remove instructions to load the Claude adapter after incorporating their approved equivalents. Verify local links and links to the upstream guides, including those in `poteto-help`.\n- If execution uncovers a platform dependency without an approved decision, record it in the review, return it to `ready-for-human`, and present it for review before delivering output.\n"]]:
>     p=Path('working/pstack/forks')/fork/'4_cursor_replacement_generalization/requirements.md'
>     assert '## Terms' in p.read_text(encoding='utf-8')
>     p.write_text(source,encoding='utf-8',newline='\n')
> '@ | uv run --no-cache --no-sync python -X utf8 -``
> - Ran `@'
> from pathlib import Path
> import runpy,sys,tempfile,contextlib,io
> ns=runpy.run_path('working/pstack/forks/review_input.py')
> g=ns['main'].__globals__
> def run(*args):
>     save=sys.argv
>     try:
>         sys.argv=['review_input.py',*args]
>         stdout,stderr=io.StringIO(),io.StringIO()
>         with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr):
>             try: code=ns['main']()
>             except SystemExit as e: code=e.code
>         return code,stdout.getvalue().strip(),stderr.getvalue().strip()
>     finally: sys.argv=save
> assert run('--preview')[1]==ns['frontmatter'].load(g['REVIEW'])['input_id']
> code,_,msg=run('--check-apply')
> assert code and 'Missing review input' in msg
> print('Real preview matches the record. Real apply is blocked while Stage 3 is missing.')
> with tempfile.TemporaryDirectory() as tmp:
>  p=Path(tmp);shared=p/'shared';g.update(SHARED=shared,ADAPTER=p/'adapter.md',REVIEW=p/'review.md')
>  tree=shared/'3_autoPR_local_fallback/output'
>  for d in ['agents','skills']:(tree/d).mkdir(parents=True)
>  (tree/'agents/a.md').write_text('original')
>  g['ADAPTER'].write_text('adapter')
>  cur=run()[1]
>  def record(status,key):g['REVIEW'].write_text(f'---\nstatus: {status}\ninput_id: {key}\n---\nKeep human decisions.\n')
>  record('ready-for-human',cur);assert run('--check-apply')[0]==1
>  record('done',cur);original=g['REVIEW'].read_bytes()
>  assert run('--check-apply')[0]==0
>  (p/'unrelated').touch();(tree/'agents/a.md').touch()
>  assert run('--check-apply')[0]==0
>  (tree/'agents/a.md').write_text('changed');assert run('--check-apply')[0]==1
>  (tree/'agents/a.md').write_text('original');(tree/'agents/a.md').rename(tree/'agents/b.md');assert run('--check-apply')[0]==1
>  (tree/'agents/b.md').rename(tree/'agents/a.md');g['ADAPTER'].write_text('new adapter')
>  assert run('--check-apply')[0]==1 and g['REVIEW'].read_bytes()==original
>  print('Passed approval, reuse, unrelated changes, touch, content change, rename and adapter change. Decisions unchanged.')
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> import re,frontmatter,subprocess
> pstack=Path('working/pstack'); forks=pstack/'forks'
> doc=forks/'adaptation-review.md'
> review=frontmatter.load(doc)
> print(review.metadata)
> defs=dict(re.findall(r'^\[([^\]]+)\]: (\S+)$',review.content,re.M))
> used=set(re.findall(r'\]\[([^\]]+)\]',review.content));assert used==set(defs),(set(defs)-used,used-set(defs))
> for link in defs.values(): assert (doc.parent/link).is_file(),link
> for f in [pstack/'README.md', *forks.glob('*/4_*/requirements.md')]:
>  for t in re.findall(r'\]\(([^\)]+)\)',f.read_text(encoding='utf-8')):
>     assert (f.parent/t.split('#')[0]).is_file(),(f,t)
> print(f'{len(defs)} evidence links and both workflow entry points verified')
> print(subprocess.run(['git','diff','--check','--','working/pstack'],capture_output=True,text=True,check=True).stdout)
> for name in ('codex','generic'):
>  assert not (forks/name/'4_cursor_replacement_generalization/output').exists()
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> root=Path('working/pstack/shared/1_extract_and_pick/output')
> p=root/'skills/poteto-mode/SKILL.md'
> for i,l in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
>  if i in (75,76,77,78,79,80,81,82,83,84,85,86,89,101,102):print(i,l[:700])
> p=root/'skills/poteto-help/SKILL.md'
> print(p.read_text(encoding='utf-8').splitlines()[49])
> for f in root.rglob('*.md'):
>  ls=f.read_text(encoding='utf-8').splitlines()
>  for i,l in enumerate(ls,1):
>     if l.startswith('In Claude Code, read '):continue
>     if any(x in l.lower() for x in ['computer use tool','browser tool','image generation tool','in-app browser','skill registry','compaction trigger','the agent window','code editor','run_in_background','client tool','session store','forced to stop','userinput','readfile','chat mentions','background terminal','stop hook','model-invocation: false']):
>         print(f.relative_to(root),i,l[:170])
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran ``@'
> from pathlib import Path
> forks=Path('working/pstack/forks')
> for p in forks.glob('*/4_*/requirements.md'):
>  s=p.read_text(encoding='utf-8').replace('Leave the review at `ready-for-human`.','Mark a new or refreshed review `ready-for-human`. Reuse an unchanged review with its existing status and human edits.')
>  p.write_text(s,encoding='utf-8',newline='\n')
> p=forks/'adaptation-review.md'
> s=p.read_text(encoding='utf-8')
> s=s.replace('以下按需要人作决定的行为合并重复调用。','适配器还规定遇到未映射的 Cursor 工具字段时省略并说明；这条规则只处理调用参数，不能单独恢复工作流所需的能力。以下按需要人作决定的行为合并重复调用。')
> key='| [Automate me][ask] `allow_multiple: true`'
> assert key in s
> s=s.replace(key,'| 适配器说明哪种子 agent 能访问 MCP。[模式入口][mode] 第 76–82 行还把团队聊天、工单更新和启动评测列入可自主执行的操作；[worker 指令][worker] 对向运行外部发消息另有停下条件。 | 分开描述父会话与 worker 的操作范围，调用目标端已授权的连接器，并保留具体动作原有的暂停条件。 | 同通用，按当前会话授权处理需要人工确认的外部写入。 |\n'+key)
> p.write_text(s,encoding='utf-8',newline='\n')
> print('Inventory and entry points checked')
> '@ | uv run --no-cache --no-sync python -X utf8 -``
>
> </details>
</details>

两个 fork 原来的 `Terms` 确实列多了。22 个 skill 入口指向同一份 Claude Code 适配器，里面已经有工具、子代理参数、模型、路径和 Cursor 专属能力的映射。旧表还列了 `/in-cloud`、`/autopilot` 和插件更新命令，在这次选入的 Markdown 里都没有实际调用点。我已把两份规格改短，并把证据和待审决定集中到一份[适配清单](./working/pstack/forks/adaptation-review.md)。

你列的六类问题都有源码依据，有三处值得补充：

- **`/loop` 涉及五个执行 playbook。** 除了自主运行、每小时审计和合并队列，Bug fix 和 Visual parity 也用了它。前几处需要唤醒或等待，后两处需要迭代到验证通过，不能统一替换成“定时检查”。
- **云端 worker 已有部分明确规则。** 适配器写了如何隔离工作树、指定起始分支，以及何时跳过需要远端机器的步骤。剩下要决定的是怎样接续 cloud-agent URL、怎样让替代 worker 读到共享记录，以及怎样传达停写。
- **还有旧清单没抓到的依赖。** 包括 `ketchup` 的 `/visualize`、多选提问、按路径触发 skill，以及模型回退后怎样满足“由另一供应商独立审查”。`worktree-audit.sh` 和 `watch-pr` 的问题也已定位到代码和测试。Routines 和内建 PR 工具则归入已有明确规则的项目。

**现在 Stage 4 分两次运行。** 第一次只调查，生成 `status: ready-for-human` 的清单。人分别编辑 Generic 和 Codex 两列，确认后改成 `done`。第二次由人明确指定执行哪个 fork，Agent 才生成该分支的产物。[Stage 4 流程](./working/pstack/README.md#stage-4)

版本判断只用一个 `input_id`，取自**第三阶段实际的 `agents/`、`skills/` 和上游适配器**。输入相同就保留人工决定，`done` 后再运行调查会直接复用。输入变化才重新核对差异，保留仍适用的决定。已验证无关提交或文件时间变化不会触发重审，文件改名、内容或适配器变化会使旧审批失效。[输入检查脚本](./working/pstack/forks/review_input.py)

**目前这份清单是预审稿。** 第三阶段还没有 `output/`，本次审查使用了第一阶段的实际文件。你现在就可以编辑目标术语；正式输入生成后会再核对差异，届时再标 `done`。

> emmmm，你的意思是搞大表吗？如果是这样，那我觉得放在最后一步，直接第二步走分发，也许会更合适？此外，还有问题，就是你这整理的也不对啊，我要的是替换表，结果你就整理了 适配器遗漏、部分遗漏的，“有上游依据的常规映射”是适配器照搬过来的吗？原来的适配器那个文件不是写的很好吗？为啥用这么抽象难懂的东西，重述一遍，然后再加上花里胡哨、繁琐的引用和描述，然后来源和目标又不匹配，又是一个词一个句子，而且句子还是建议，我要直接修改你预填的。说实话，一塌糊涂

<details><summary>7 previous messages</summary>

> 上一版把证据、建议和替换文本混在了一起，确实没法直接改。我会按上游适配器的写法重做，让每行左边是原文、右边是可直接采用的替换文本，并把分发和最终替换的顺序理清。
>
> <details><summary>Ran 2 commands</summary>
>
> - Ran `@'
> from pathlib import Path
> for p in [Path('working/pstack/README.md'),*Path('working/pstack').rglob('requirements.md'),Path('working/pstack/forks/review_input.py')]:
>  print(p.as_posix(),p.read_text(encoding='utf-8')[:(4200 if 'forks' in p.parts or p.name=='README.md' else 700)])
> print('DIRS', [p.as_posix() for p in Path('working/pstack').glob('*/*/*') if p.is_dir() and p.name!='output'])
>
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> import subprocess
> root=Path('sources/cursor-plugins/harness/pstack/claude-code')
> print((root/'docs/harness/claude-code.md').read_text(encoding='utf-8'))
> print(subprocess.run(['git','status','--short','--ignore-submodules','--','working/pstack'],capture_output=True,text=True).stdout[:2700])
>
> '@ | uv run --no-cache --no-sync python -X utf8 -`
>
> </details>
>
> 你说的“第二步走分发”，我理解为最后一个阶段里，第一步审定替换表，第二步按列直接生成 Generic 和 Codex 两份产物。还是指整个流水线在提取后的第 2 阶段就分叉？
> - 最终阶段审表，再分发两版
> - 提取后第 2 阶段就分叉
>
> <details><summary>Ran 2 commands</summary>
>
> - Ran `@'
> from pathlib import Path
> root=Path('working/pstack/shared/1_extract_and_pick/output')
> def show(name,indices):
>  print('\n'+name)
>  ls=(root/name).read_text(encoding='utf-8').splitlines()
>  for n in indices:
>     if n<=len(ls):print(n,ls[n-1])
> for n,nums in [('skills/arena/SKILL.md',[19,24,30]),('skills/setup-pstack/SKILL.md',[10,16,50,54,55,60,61,62,63,64,65,66,67,68,69,70,71]),('skills/poteto-mode/playbooks/autopilot-full.md',[8,10,12,14,22]),('skills/poteto-mode/playbooks/shipping.md',[5,9]),('skills/poteto-mode/playbooks/session-pickup.md',[5]),('skills/poteto-mode/playbooks/worktree-cleanup.md',[4,5,8]),('skills/poteto-mode/scripts/worktree-audit.sh',[71,72,73,74,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128]),('skills/poteto-mode/references/bugbot-triage.md',range(20,36)),('skills/poteto-mode/playbooks/babysit.md',[6,9])]:show(n,nums)
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> root=Path('working/pstack/shared/1_extract_and_pick/output')
> def show(name,indices):
>  print('\n'+name)
>  ls=(root/name).read_text(encoding='utf-8').splitlines()
>  for n in indices:
>     if n<=len(ls):print(n,ls[n-1])
> for name,nums in [('skills/how/SKILL.md',[9,11,13,15]),('skills/no-comments/SKILL.md',[9,13,15,17,19]),('skills/recall/SKILL.md',[17,22]),('skills/swarm/SKILL.md',[13,24,29,31]),('skills/poteto-mode/SKILL.md',[22,26,27,29,88,90,100,102,110]),('skills/automate-me/SKILL.md',[13,19,31,46,48,69,71,75]),('skills/poteto-help/SKILL.md',[15,40,44,48,56,58,59,60,118,119,120,133,135]),('agents/poteto-agent.md',[3,4,5,10])]:show(name,nums)
> '@ | uv run --no-cache --no-sync python -X utf8 -`
>
> </details>
>
> **你说的“第二步走分发”，我理解为最后一个阶段里，第一步审定替换表，第二步按列直接生成 Generic 和 Codex 两份产物。还是指整个流水线在提取后的第 2 阶段就分叉？**
>
> 阶段，是stage，步是一个stage内部的，我不知道你在问啥
>
> 明白了：前面的 stage 仍然共享，最后一个 stage 内，第一步预填替换表供你修改，第二步按定稿直接分发两版。Codex 的 `openai.yaml` 也放进这个分发步骤。
>
> <details><summary>Ran 11 commands</summary>
>
> - Ran `@'
> import subprocess
> from pathlib import Path
> p=subprocess.run(['rg','-l','--hidden','-g','!.git','-g','!sources/**','-g','!.venv','-g','!**/output/**','-g','!releases/**','4_cursor_replacement|5_codex_agent|forks/review_input|adaptation-review|Stage 4|stage-4|forks/generic/dependencies'],capture_output=True,text=True);print(p.stdout)
> for d in sorted(Path('working/pstack/forks').rglob('*')):
>  if d.is_file(): print(d.as_posix(),d.stat().st_size)
> root=Path('working/pstack/shared/1_extract_and_pick/output')
> for p in sorted(root.rglob('*.md')):
>  name=p.relative_to(root).as_posix()
>  for i,l in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
>     if any(s in l for s in ['Spawn one Task','Grep','Glob','Use the **create-skill**','SendToUser','/loop','/visualize','cloud_base_branch','file_attachments','AskQuestion','readonly: true','subagent_type:']) and (len(l)<420 or 'Spawn one Task' in l):
>         print(name,i,l[:440])
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> import re
> for base in [Path('working'),Path('sources')]:
>  files=base.rglob('*.md') if base.name=='working' else base.glob('*.md')
>  for f in files:
>     if 'output' in f.parts:continue
>     lines=f.read_text(encoding='utf-8').splitlines()
>     for i,l in enumerate(lines,1):
>         if re.search(r'4_cursor_replacement|5_codex_agent|review_input\.py|adaptation-review|forks/(?:generic|codex)|stage.?4',l,re.I):print(f.as_posix(),i,l[:160])
> root=Path('working/pstack/shared/1_extract_and_pick/output')
> for x in ['skills/create-verification-skill/SKILL.md','skills/make-bot-ui/SKILL.md','skills/poteto-mode/playbooks/bug-fix.md','skills/poteto-mode/playbooks/opening-a-pr.md','skills/poteto-mode/playbooks/eval.md','skills/reflect/SKILL.md','skills/poteto-mode/playbooks/visual-parity.md']:
>  for i,l in enumerate((root/x).read_text(encoding='utf-8').splitlines(),1):
>     if any(t in l for t in ['.cursor','update_state','secret-request','sender key','/loop','draft: false','plugins/cache','/deslop']):
>         print(x,i,l[:800])
>
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> base=Path('working/pstack').resolve(strict=True)
> stage=base/'shared/4_adapt_and_distribute'
> assert not stage.exists()
> stage.mkdir()
> forks=base/'forks'
> for src,dest in [(forks/'review_input.py', stage/'review_input.py'), (forks/'adaptation-review.md',stage/'replacements.md'), (forks/'generic/4_cursor_replacement_generalization/requirements.md',stage/'requirements.md')]:
>     assert src.resolve().is_relative_to(base) and dest.resolve().parent == stage
>     src.rename(dest)
> helper=stage/'review_input.py'
> s=helper.read_text(encoding='utf-8').replace('FORKS = Path(__file__).resolve().parent','STAGE = Path(__file__).resolve().parent').replace('SHARED = FORKS.parent / "shared"','SHARED = STAGE.parent').replace('FORKS.parents[2]','STAGE.parents[3]').replace('REVIEW = FORKS / "adaptation-review.md"','REVIEW = STAGE / "replacements.md"')
> helper.write_text(s,encoding='utf-8',newline='\n')
>
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> s=Path('working/pstack/shared/1_extract_and_pick/output/skills')
> for name in ('poteto-mode/scripts/worktree-audit.sh','poteto-mode/SKILL.md','make-bot-ui/SKILL.md','poteto-mode/playbooks/authoring-a-skill.md','poteto-mode/playbooks/visual-parity.md','typescript-best-practices/SKILL.md','ketchup/SKILL.md'):
>  ls=(s/name).read_text(encoding='utf-8').splitlines()
>  nums={'poteto-mode/scripts/worktree-audit.sh':[19,20,21,22,30,72,73,74,114,124,125],'poteto-mode/SKILL.md':[5,6,105,106,107], 'make-bot-ui/SKILL.md':[15,17,27,29,33,34,35,36,37,39,41,43,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60], 'typescript-best-practices/SKILL.md':[2,3,4], 'ketchup/SKILL.md':[43], 'poteto-mode/playbooks/authoring-a-skill.md':[5], 'poteto-mode/playbooks/visual-parity.md':[8]}
>  print(name)
>  for n in nums[name]:print(n,ls[n-1])
>
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> p=Path('working/pstack/shared/1_extract_and_pick/output')
> doc=p/'skills/poteto-mode/playbooks/worktree-cleanup.md'
> print(doc.read_text(encoding='utf-8').splitlines()[2])
> for nm in ('skills/poteto-mode/SKILL.md','skills/poteto-help/SKILL.md','skills/poteto-mode/playbooks/autonomous-run.md','skills/poteto-mode/playbooks/shipping.md'):
>  for l in (p/nm).read_text(encoding='utf-8').splitlines():
>     if ('routine' in l or 'slash menu' in l or 'orchestrate' in l or 'remote machine' in l or 'cloud agent' in l):
>         print(nm, l[:500])
> print(Path('working/pstack/forks/generic/dependencies.md').read_text(encoding='utf-8'))
>
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran ``@'
> from pathlib import Path
> root=Path('working/pstack/shared/1_extract_and_pick/output')
> texts=[p.read_text(encoding='utf-8',errors='replace') for p in root.rglob('*') if p.is_file()]
> rows=["Open a todolist with one entry per phase before launching anything.","Copy its steps into the todolist tool first.","Spawn one Task subagent with `subagent_type: generalPurpose` and `readonly: true` that explores and explains in one pass.","Spawn `Task` with `subagent_type: \"comment-sicko\"`.","Use `subagent_type: \"poteto-agent\"` for any subagent you spawn directly inside a playbook step.","in agent mode because readonly strips MCP access","`allow_multiple: true` for category questions","Use the `AskQuestion` tool (structured multi-choice) rather than asking the user to type from scratch.","If the slash menu shows `/orchestrate`, another plugin provides it.","~/.cursor/skills/",".cursor/skills/","~/.cursor/rules/pstack-models.mdc","Write `~/.cursor/rules/pstack-models.mdc`, an always-applied rule that sets pstack's model per role.","Write `~/.cursor/rules/pstack-models.mdc` with `alwaysApply: true`, the `# defaults: 3` line, a `# budget` line with the chosen label and the effort that label names, and one line per role, using the same labels poteto-mode uses.","If Cursor also exposes a models API or CLI that lists the user's entitled models, prefer it for completeness.","Families go by prefix, and the longest match wins: `claude-fable-*`, `claude-*`, and `gemini-*`, after dropping a leading `cursor-`.","A second opinion is the same prompt on another vendor's model.","If more than one file matches, use the copy whose `.cursor-plugin/plugin.json` has the highest `version`.","With no path, before any other work, search `~/.cursor/plugins/` for a file whose path ends in `skills/poteto-mode/SKILL.md`.","Use Cursor's built-in `create-skill` skill to author the skill.","Use the **create-skill** skill (Cursor's built-in for authoring SKILL.md files).","Spawn all N workers in one message with `subagent_type: generalPurpose`, `environment: \"cloud\"`, `run_in_background: true`, and the step 3 model, left unset for `auto` or `inherit-parent`.","Use `environment: \"local\"` only when the worker needs access to something on the user's computer.","When a worker must start from a non-default pushed branch, pass `cloud_base_branch`.","a Cursor cloud agent","the root agent's store (path in the system prompt)","a cloud-agent URL, or a pushed branch","Resume an existing subagent only when the work needs state that lives in it and is costly to move: its checkout, its uncommitted changes, or a process it still runs.","Pick the wake mechanism using Cursor's `/loop` command (a built-in, not a pstack skill).","On the operator's go, arm `/loop 1h` to audit until no delegated work is left, because long runs drift and agents stall silently.","watch the run with `scripts/watch-pr/watch-pr --queued-stack` under `/loop` until it reports `COMPLETE` at the ceiling","Drive a long or stubborn hunt with Cursor's `/loop` command.","`/loop` per component until the diff is zero.","Run `/deslop` from `cursor-team-kit` over the diff before commit.","Before commit → `/deslop` from the `cursor-team-kit` plugin.","the slop-strip (the `deslop` skill from the `cursor-team-kit` plugin (`/deslop`))","Shipping UI / IDE / CLI → `control-ui` or `control-cli` from `cursor-team-kit`.","its control skill (such as `control-ui` or `control-cli` from `cursor-team-kit`) or a named driver","a `/visualize` chart for numbers","Open PRs ready, through the run's PR tool with `draft: false`.","The system prompt names the workspace's `agent-transcripts/` directory. Use only that path. Don't glob across `~/.cursor/projects/*/`.","Transcripts live at `~/.cursor/projects/<slug>/agent-transcripts/<uuid>/<uuid>.jsonl`, where `<slug>` is the workspace path with the leading slash dropped and each \"/\" turned into \"-\" (so `/Users/you/proj` becomes `Users-you-proj`). Every line is one chat message.","Get that set from the user or sidebar and cross-check every candidate.","The transcript scan is slow, so background it.","Triage Bugbot skeptically: fix real findings, dismiss noise with a concrete disproof, escalate billing, data, auth, and security.","Install with `/add-plugin pstack` in chat, or from Customize in the sidebar.","Enter on `/poteto-mode` attaches the skill to one message. It fades as the chat moves on.","Option+Enter on Mac or Alt+Enter on Windows, or Use as Mode from the skill entry, makes it a Custom Mode. It stays in context every turn until the user exits the mode, and it stays out of casual turns.","pstack has no planning skill. Cursor's Plan Mode works alongside it.","Cursor's built-in babysit skill","../../docs/guide/","../../README.md","Call `update_state` with target `routine` and action `create`.","The webhook URL and the sender key live on that routine's panel after the routine exists.","Do not accept the sender key in chat. Send a secret-request, then stop. That card is the whole turn."]
> print('unmatched',[row for row in rows if not any(row in s for s in texts)])
> for p in (root/'skills/poteto-mode/SKILL.md',root/'skills/arena/SKILL.md',root/'skills/poteto-help/SKILL.md'):
>  for i,l in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
>     if 'Grep' in l or 'Glob' in l or 'cloud agent' in l: print(p.name,i,l[:380])
>
> '@ | uv run --no-cache --no-sync python -X utf8 -``
> - Ran `@'
> from pathlib import Path
> r=Path('working/pstack/shared/1_extract_and_pick/output')
> for s in ['skills/poteto-mode/SKILL.md','skills/setup-pstack/SKILL.md','skills/make-bot-ui/SKILL.md','skills/poteto-mode/playbooks/authoring-a-skill.md']:
>  t=(r/s).read_text(encoding='utf-8').splitlines()
>  for i,l in enumerate(t,1):
>     if (s.startswith('skills/setup') and i in range(49,60)) or (s.startswith('skills/make-bot') and (14<=i<=37 or i in (93,94,109))) or ('bind' in l):print(i,l[:420])
> for line in (r/'skills/poteto-help/SKILL.md').read_text(encoding='utf-8').splitlines():
>  if 'Whether ' in line or 'new task' in line or 'claude' in line.lower(): print(line[:500])
>
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran ``@'
> from pathlib import Path
> import json
> stage=Path('working/pstack/shared/4_adapt_and_distribute')
> root=stage.parent/'1_extract_and_pick/output'
> files=[f.read_text(encoding='utf-8',errors='replace') for f in root.rglob('*') if f.is_file()]
> rows=["Task tool","Prefer AskQuestion over free text.","Open a todolist with one entry per phase before launching anything.","Copy its steps into the todolist tool first.","Spawn one Task subagent with `subagent_type: generalPurpose` and `readonly: true` that explores and explains in one pass.","Spawn `Task` with `subagent_type: \"comment-sicko\"`.","Use `subagent_type: \"poteto-agent\"` for any subagent you spawn directly inside a playbook step.","in agent mode because readonly strips MCP access","`allow_multiple: true` for category questions","Use the `AskQuestion` tool (structured multi-choice) rather than asking the user to type from scratch.","~/.cursor/skills/",".cursor/skills/","~/.cursor/rules/pstack-models.mdc","Write `~/.cursor/rules/pstack-models.mdc` with `alwaysApply: true`, the `# defaults: 3` line, a `# budget` line with the chosen label and the effort that label names, and one line per role, using the same labels poteto-mode uses.","If Cursor also exposes a models API or CLI that lists the user's entitled models, prefer it for completeness.","Families go by prefix, and the longest match wins: `claude-fable-*`, `claude-*`, and `gemini-*`, after dropping a leading `cursor-`.","A second opinion is the same prompt on another vendor's model.","If more than one file matches, use the copy whose `.cursor-plugin/plugin.json` has the highest `version`.","With no path, before any other work, search `~/.cursor/plugins/` for a file whose path ends in `skills/poteto-mode/SKILL.md`.","Use Cursor's built-in `create-skill` skill to author the skill.","Use the **create-skill** skill (Cursor's built-in for authoring SKILL.md files).","For `auto` or `inherit-parent`, omit `model` so the workers run on the parent model.","If the Task tool rejects a slug, use the default and say so.","Spawn all N workers in one message with `subagent_type: generalPurpose`, `environment: \"cloud\"`, `run_in_background: true`, and the step 3 model, left unset for `auto` or `inherit-parent`.","Use `environment: \"local\"` only when the worker needs access to something on the user's computer.","When a worker must start from a non-default pushed branch, pass `cloud_base_branch`.","a Cursor cloud agent","the root agent's store (path in the system prompt)","a cloud-agent URL, or a pushed branch","Resume an existing subagent only when the work needs state that lives in it and is costly to move: its checkout, its uncommitted changes, or a process it still runs.","Give each agent its own worktree, or run them as cloud agents, which each get their own machine.","`run_in_background: true`, agent mode (readonly strips MCP), file pointers not inlined context, and an explicit model per role, Project workers included.","Pick the wake mechanism using Cursor's `/loop` command (a built-in, not a pstack skill).","On the operator's go, arm `/loop 1h` to audit until no delegated work is left, because long runs drift and agents stall silently.","watch the run with `scripts/watch-pr/watch-pr --queued-stack` under `/loop` until it reports `COMPLETE` at the ceiling","Drive a long or stubborn hunt with Cursor's `/loop` command.","`/loop` per component until the diff is zero.","Run `/deslop` from `cursor-team-kit` over the diff before commit.","Before commit → `/deslop` from the `cursor-team-kit` plugin.","the slop-strip (the `deslop` skill from the `cursor-team-kit` plugin (`/deslop`))","Shipping UI / IDE / CLI → `control-ui` or `control-cli` from `cursor-team-kit`.","its control skill (such as `control-ui` or `control-cli` from `cursor-team-kit`) or a named driver","a `/visualize` chart for numbers","Open PRs ready, through the run's PR tool with `draft: false`.","The system prompt names the workspace's `agent-transcripts/` directory. Use only that path. Don't glob across `~/.cursor/projects/*/`.","Transcripts live at `~/.cursor/projects/<slug>/agent-transcripts/<uuid>/<uuid>.jsonl`, where `<slug>` is the workspace path with the leading slash dropped and each \"/\" turned into \"-\" (so `/Users/you/proj` becomes `Users-you-proj`). Every line is one chat message.","Get that set from the user or sidebar and cross-check every candidate.","The transcript scan is slow, so background it.","Triage Bugbot skeptically: fix real findings, dismiss noise with a concrete disproof, escalate billing, data, auth, and security.","Install with `/add-plugin pstack` in chat, or from Customize in the sidebar.","Enter on `/poteto-mode` attaches the skill to one message. It fades as the chat moves on.","Option+Enter on Mac or Alt+Enter on Windows, or Use as Mode from the skill entry, makes it a Custom Mode. It stays in context every turn until the user exits the mode, and it stays out of casual turns.","pstack has no planning skill. Cursor's Plan Mode works alongside it.","Cursor's built-in babysit skill","../../docs/guide/","../../README.md","Call `update_state` with target `routine` and action `create`.","The webhook URL and the sender key live on that routine's panel after the routine exists.","Do not accept the sender key in chat. Send a secret-request, then stop. That card is the whole turn.","1. Click this agent's name in the chat header, or press **Cmd+Shift+I**.\n2. Find the **Routines** list under the computer preview.\n3. Open this webhook routine.\n4. Copy the webhook URL. The user may paste the URL in chat.\n5. Copy the sender key. The user must not paste the sender key in chat.","SendToUser\ntype: secret-request\nsecret.label: webhook sender key\nsecret.connector: <routine folder slug>\nsecret.field: key","pstack has no `/orchestrate` skill. If the slash menu shows `/orchestrate`, another plugin provides it.","# Transcripts dir: ~/.cursor/projects/<slugified-repo-path>/agent-transcripts.","slug=$(printf '%s' \"$main_wt\" | sed 's#^/##; s#/#-#g')","transcripts=\"$HOME/.cursor/projects/$slug/agent-transcripts\"","if [ \"$recent\" = yes ]; then bucket=verify-recent-chat","CURSOR_AUTOMATION_ID","---\ndescription: pstack per-role model choices (overrides skill defaults)\nalwaysApply: true\n---","icon: crown\ncolor: yellow","paths: [\"**/*.ts\", \"**/*.tsx\"]","is_background: true","model: claude-opus-5-5-xhigh-fast"]
> missing=[s for s in rows if not any(s in f for f in files)]
> if missing:raise ValueError(missing)
> assert len(set(rows))==len(rows)
> p=stage/'replacements.md';before=p.read_text(encoding='utf-8')
> assert 'input_id: preview-aec144bbf1048751b77fe5a60e268eedd526cd110e957ccb4b696de506885011' in before
> p.write_text("---\nstatus: ready-for-human\ninput_id: preview-aec144bbf1048751b77fe5a60e268eedd526cd110e957ccb4b696de506885011\n---\n\n# pstack 替换表\n\n直接编辑右栏。“两版”同时用于 Generic 和 Codex；只有目标文字不同的条目分列在最后。`∅` 表示删除该段或字段。当前原文取自第一阶段，第三阶段产物生成后核对一次。\n\n## 调用与提问\n\n| 原文 | 两版替换为 |\n| --- | --- |\n| Open a todolist with one entry per phase before launching anything. | Create a checklist with one item per phase before launching any workers. |\n| Copy its steps into the todolist tool first. | Copy its steps into the task checklist first. |\n| Spawn one Task subagent with `subagent_type: generalPurpose` and `readonly: true` that explores and explains in one pass. | Give one general-purpose subagent a read-only pass to explore the code and explain it. |\n| Spawn `Task` with `subagent_type: \"comment-sicko\"`. | Give the review to a subagent using the instructions in `agents/comment-sicko.md`. |\n| Use `subagent_type: \"poteto-agent\"` for any subagent you spawn directly inside a playbook step. | Give each subagent you start directly inside a playbook step the instructions in `agents/poteto-agent.md`. |\n| in agent mode because readonly strips MCP access | with read access to that source through MCP |\n| `allow_multiple: true` for category questions | let the user select several categories in one reply |\n\n## Skills 和模型配置\n\n| 原文 | 两版替换为 |\n| --- | --- |\n| ~/.cursor/skills/ | ~/.agents/skills/ |\n| .cursor/skills/ | .agents/skills/ |\n| ~/.cursor/rules/pstack-models.mdc | ~/.agent/pstack-models.md |\n| Write `~/.cursor/rules/pstack-models.mdc` with `alwaysApply: true`, the `# defaults: 3` line, a `# budget` line with the chosen label and the effort that label names, and one line per role, using the same labels poteto-mode uses. | Write `~/.agent/pstack-models.md` with the `# defaults: 3` line, the chosen `# budget` line, and one line per role using the labels in poteto-mode. |\n| If Cursor also exposes a models API or CLI that lists the user's entitled models, prefer it for completeness. | List the models available to workers in this session. |\n| Families go by prefix, and the longest match wins: `claude-fable-*`, `claude-*`, and `gemini-*`, after dropping a leading `cursor-`. | Use the model catalog’s family and provider names. Count Fable and Opus as separate families from the same provider. |\n| A second opinion is the same prompt on another vendor's model. | For a second opinion, send the same prompt to a model from another provider. If none is available, report that the independent review could not run. |\n| If more than one file matches, use the copy whose `.cursor-plugin/plugin.json` has the highest `version`. | If several copies match, ask the parent which installation it used. |\n| With no path, before any other work, search `~/.cursor/plugins/` for a file whose path ends in `skills/poteto-mode/SKILL.md`. | If the parent supplied no path, look for `poteto-mode/SKILL.md` in the project and user skill directories before starting work. |\n| For `auto` or `inherit-parent`, omit `model` so the workers run on the parent model. | For `auto` or `inherit-parent`, let each worker inherit the parent model. |\n| If the Task tool rejects a slug, use the default and say so. | If the worker launcher rejects a model ID, use the role default and report the change. |\n\n## 后台 worker 与接续\n\n| 原文 | 两版替换为 |\n| --- | --- |\n| Spawn all N workers in one message with `subagent_type: generalPurpose`, `environment: \"cloud\"`, `run_in_background: true`, and the step 3 model, left unset for `auto` or `inherit-parent`. | Start all N general-purpose workers together on remote machines. Run them in the background with the step 3 model, inheriting the parent model for `auto` or `inherit-parent`. |\n| Use `environment: \"local\"` only when the worker needs access to something on the user's computer. | Run a worker locally only when it needs something on the user’s computer. |\n| When a worker must start from a non-default pushed branch, pass `cloud_base_branch`. | Name the pushed branch in the brief and have the worker check it out before starting. |\n| the root agent's store (path in the system prompt) | the shared decision log named in the kickoff |\n| a cloud-agent URL, or a pushed branch | a link to the prior worker’s session, or a pushed branch |\n| Resume an existing subagent only when the work needs state that lives in it and is costly to move: its checkout, its uncommitted changes, or a process it still runs. | Resume the same worker when the task needs its checkout, uncommitted changes, or a running process. If you cannot reconnect, report which state is unavailable. |\n| Give each agent its own worktree, or run them as cloud agents, which each get their own machine. | Give each local worker a separate worktree. If a task needs a remote machine and none is available, report that worker as blocked. |\n| `run_in_background: true`, agent mode (readonly strips MCP), file pointers not inlined context, and an explicit model per role, Project workers included. | Launch workers in the background, give them the MCP access their task requires, pass file paths in the brief, and select the model for their role. |\n\n## 等待与验证\n\n| 原文 | 两版替换为 |\n| --- | --- |\n| Pick the wake mechanism using Cursor's `/loop` command (a built-in, not a pstack skill). | Choose what will wake this run: a watched event with a backup timer, or a fixed interval. |\n| On the operator's go, arm `/loop 1h` to audit until no delegated work is left, because long runs drift and agents stall silently. | Once the operator gives the go-ahead, audit every hour until all delegated work has finished. |\n| watch the run with `scripts/watch-pr/watch-pr --queued-stack` under `/loop` until it reports `COMPLETE` at the ceiling | keep running `scripts/watch-pr/watch-pr --queued-stack` until it reports `COMPLETE` at the ceiling |\n| Drive a long or stubborn hunt with Cursor's `/loop` command. | Repeat the investigation until runtime evidence isolates the cause. |\n| `/loop` per component until the diff is zero. | Repeat the image comparison for each component until its diff is zero. |\n| Run `/deslop` from `cursor-team-kit` over the diff before commit. | Before committing, review the diff and remove unnecessary generated code. |\n| Before commit → `/deslop` from the `cursor-team-kit` plugin. | Before commit → review the diff and remove unnecessary generated code. |\n| the slop-strip (the `deslop` skill from the `cursor-team-kit` plugin (`/deslop`)) | the cleanup pass over the diff |\n| Shipping UI / IDE / CLI → `control-ui` or `control-cli` from `cursor-team-kit`. | Shipping UI / IDE / CLI → drive the actual interface or invoke the CLI with representative input and record the result. |\n| its control skill (such as `control-ui` or `control-cli` from `cursor-team-kit`) or a named driver | a named driver for the actual UI or CLI |\n| a `/visualize` chart for numbers | a chart of the measured values |\n| Open PRs ready, through the run's PR tool with `draft: false`. | Open each PR as ready for review using the session’s PR tool. |\n\n## 会话、清理与审查\n\n| 原文 | 两版替换为 |\n| --- | --- |\n| The system prompt names the workspace's `agent-transcripts/` directory. Use only that path. Don't glob across `~/.cursor/projects/*/`. | Read only conversations belonging to the active workspace. |\n| Get that set from the user or sidebar and cross-check every candidate. | Cross-check every candidate against the active and pinned sessions. Ask the user for the set if you cannot read it. |\n| The transcript scan is slow, so background it. | Set `PSTACK_TRANSCRIPT_DIR` to this workspace’s transcript directory for the audit, then run the scan in the background. If you cannot obtain that directory, keep candidates for manual review. |\n| Triage Bugbot skeptically: fix real findings, dismiss noise with a concrete disproof, escalate billing, data, auth, and security. | Triage existing review threads: fix real findings, dismiss noise with a concrete disproof, and escalate billing, data, auth, and security. Skip Bugbot-specific waits when the PR has no Bugbot check or comment. |\n\n## 帮助与 webhook\n\n| 原文 | 两版替换为 |\n| --- | --- |\n| Enter on `/poteto-mode` attaches the skill to one message. It fades as the chat moves on. | Invoke the **poteto-mode** skill at the start of a task. |\n| Option+Enter on Mac or Alt+Enter on Windows, or Use as Mode from the skill entry, makes it a Custom Mode. It stays in context every turn until the user exits the mode, and it stays out of casual turns. | For a later task, invoke **poteto-mode** again. |\n| pstack has no planning skill. Cursor's Plan Mode works alongside it. | For planning-only work, run the **Multi-phase plan** playbook. |\n| Cursor's built-in babysit skill | a host-provided PR monitor |\n| ../../docs/guide/ | https://github.com/cursor/plugins/blob/main/harness/pstack/claude-code/docs/guide/ |\n| ../../README.md | https://github.com/cursor/plugins/blob/main/harness/pstack/claude-code/README.md |\n| Call `update_state` with target `routine` and action `create`. | Create a webhook-triggered routine. If this host has no webhook routines, report the skipped setup and leave the webhook URL and sender key as placeholders. |\n| The webhook URL and the sender key live on that routine's panel after the routine exists. | After the routine exists, open its settings to obtain the webhook URL and sender key. |\n| Do not accept the sender key in chat. Send a secret-request, then stop. That card is the whole turn. | Request the sender key through secure credential entry. If secure entry is unavailable, leave the key as a placeholder and report the skipped handoff. |\n| 1. Click this agent's name in the chat header, or press **Cmd+Shift+I**.<br>2. Find the **Routines** list under the computer preview.<br>3. Open this webhook routine.<br>4. Copy the webhook URL. The user may paste the URL in chat.<br>5. Copy the sender key. The user must not paste the sender key in chat. | 1. Open the webhook settings for the routine you created.<br>2. Copy its endpoint URL.<br>3. Transfer the sender key through secure credential entry. |\n| SendToUser<br>type: secret-request<br>secret.label: webhook sender key<br>secret.connector: <routine folder slug><br>secret.field: key | ∅ |\n| pstack has no `/orchestrate` skill. If the slash menu shows `/orchestrate`, another plugin provides it. | The **Swarm** skill coordinates pstack workers. The `/orchestrate` command belongs to a separate plugin. |\n\n## 文件中的代码与元数据\n\n| 原文 | 两版替换为 |\n| --- | --- |\n| `# Transcripts dir: ~/.cursor/projects/<slugified-repo-path>/agent-transcripts.` | `# PSTACK_TRANSCRIPT_DIR contains transcripts for the workspace being audited.` |\n| `slug=$(printf '%s' \"$main_wt\" \\| sed 's#^/##; s#/#-#g')` | ∅ |\n| `transcripts=\"$HOME/.cursor/projects/$slug/agent-transcripts\"` | `transcripts=\"${PSTACK_TRANSCRIPT_DIR:-}\"` |\n| `if [ \"$recent\" = yes ]; then bucket=verify-recent-chat` | `if [ \"$last_ts\" -eq 0 ] \\|\\| [ \"$recent\" = yes ]; then bucket=verify-recent-chat` |\n| `CURSOR_AUTOMATION_ID` | `CURSOR_AUTOMATION_ID` |\n| `---`<br>`description: pstack per-role model choices (overrides skill defaults)`<br>`alwaysApply: true`<br>`---` | ∅ |\n| `icon: crown`<br>`color: yellow` | ∅ |\n| `paths: [\"**/*.ts\", \"**/*.tsx\"]` | `paths: [\"**/*.ts\", \"**/*.tsx\"]` |\n| `is_background: true` | ∅ |\n\n## 两版用词不同的条目\n\n| 原文 | Generic | Codex |\n| --- | --- | --- |\n| Task tool | subagent launcher | `spawn_agent` tool |\n| Prefer AskQuestion over free text. | Present the choices as a structured question. | Use `request_user_input` when available. Otherwise ask in chat. |\n| Use the `AskQuestion` tool (structured multi-choice) rather than asking the user to type from scratch. | Present the choices in chat so the user can answer by number. | Use the session’s structured question tool when available. Otherwise list the choices in chat. |\n| Use Cursor's built-in `create-skill` skill to author the skill. | Write the skill in `SKILL.md` and validate its frontmatter and references. | Use `skill-creator` to write the skill and validate its frontmatter and references. |\n| Use the **create-skill** skill (Cursor's built-in for authoring SKILL.md files). | Create or edit the skill’s `SKILL.md`. | Use the **skill-creator** skill to create or edit `SKILL.md`. |\n| a Cursor cloud agent | a remote agent | a remote worker |\n| Transcripts live at `~/.cursor/projects/<slug>/agent-transcripts/<uuid>/<uuid>.jsonl`, where `<slug>` is the workspace path with the leading slash dropped and each \"/\" turned into \"-\" (so `/Users/you/proj` becomes `Users-you-proj`). Every line is one chat message. | Read the transcripts for this workspace, including its subagent conversations. | Select chats for this project. Open the relevant chat and its subagent records to inspect messages and tool calls. |\n| Install with `/add-plugin pstack` in chat, or from Customize in the sidebar. | Install the agents and skills from the Generic distribution. | Install the agents and skills from the Codex distribution. |\n| `model: claude-opus-5-5-xhigh-fast` | `model: claude-opus-5-5-xhigh-fast` | ∅ |\n",encoding='utf-8',newline='\n')
> print(f'{len(rows)} distinct literal sources verified')
> '@ | uv run --no-cache --no-sync python -X utf8 -``
> - Ran ````@'
> from pathlib import Path
> base=Path('working/pstack').resolve(strict=True);stage=base/'shared/4_adapt_and_distribute'
> (stage/'requirements.md').write_text("# Stage 4 · 替换与分发\n\n## 第一步 · 预填替换表\n\n输入是 `../3_autoPR_local_fallback/output/` 下的 `agents/` 和 `skills/`。[Claude Code 适配器](../../../../sources/cursor-plugins/harness/pstack/claude-code/docs/harness/claude-code.md) 用来核对已有的翻译和后备行为。\n\n在仓库根目录运行 `uv run --locked working/pstack/shared/4_adapt_and_distribute/review_input.py`。编号与[替换表](replacements.md)的 `input_id` 一致时，直接复用表和当前状态。编号变化时，核对新增、修改、移除的原文，保留仍适用的人工定稿。第三阶段尚无产物时可用 `--preview` 先填第一阶段的原文。\n\n左栏逐字取自输入，右栏预填可直接写回的词、指令或代码。两版相同的只写一次。把表标为 `ready-for-human`，停在这里。人修改右栏，审定正式输入后改为 `done`。\n\n## 第二步 · 分发\n\n收到人的分发指令后，运行同一脚本并加 `--check-apply`。检查通过后，从 Stage 3 原件分别生成 `../../forks/generic/output/` 和 `../../forks/codex/output/`。\n\n- 先套用整句和代码块，再处理其中未被替换的短词。同一动作的其他调用点沿用定稿，包括 playbook、帮助、脚本与模板。文件路径按所属目录匹配。保留原步骤的验证条件、停止条件、权限和第三阶段加入的本地后备。\n- 删除各入口中指向 Claude 适配器的引导段。检查包内链接、上游指南链接和修改过的脚本。Bugbot 轮次键和测试样例按其真实协议保留。\n- 在 Codex 产物中，对 frontmatter 含 `disable-model-invocation: true` 且缺少 `agents/openai.yaml` 的 skill，写入以下文件。已有文件保留原内容。\n\n```yaml\npolicy:\n  allow_implicit_invocation: false\n```\n",encoding='utf-8',newline='\n')
> (base/'README.md').write_text("# pstack 适配流程\n\n| Stage | 输入 | 产物 |\n| --- | --- | --- |\n| [1 · 提取](shared/1_extract_and_pick/requirements.md) | 上游 Claude Code 目录 | 完整的 `agents/`、`skills/` |\n| [2 · 统一工作文件路径](shared/2_.agent_convention/requirements.md) | Stage 1 产物 | 采用项目路径约定的共享目录 |\n| [3 · 提取 open-a-pr](shared/3_autoPR_local_fallback/requirements.md) | Stage 2 产物 | 带本地合并后备的共享目录 |\n| [4 · 替换与分发](shared/4_adapt_and_distribute/requirements.md) | Stage 3 产物 | `forks/generic/output/`、`forks/codex/output/` |\n\n最后一个 stage 有两步。第一步预填[替换表](shared/4_adapt_and_distribute/replacements.md)，由人编辑右栏并标记 `done`。第二步在收到分发指令后按这张表生成两个版本。通用版沿用[运行依赖表](forks/generic/dependencies.md)。\n",encoding='utf-8',newline='\n')
> folded=[('forks/codex/4_cursor_replacement_generalization','Adapt pstack for Codex'),('forks/codex/5_codex_agent_subdir_complement','Add Codex invocation policy')]
> for rel,signature in folded:
>     folder=base/rel
>     file=folder/'requirements.md'
>     assert file.resolve().is_relative_to(base) and signature in file.read_text(encoding='utf-8').splitlines()[0]
>     assert list(folder.iterdir())==[file]
> for rel,_ in folded:
>     folder=base/rel
>     (folder/'requirements.md').unlink()
>     folder.rmdir()
> (base/'forks/generic/4_cursor_replacement_generalization').rmdir()
>
> '@ | uv run --no-cache --no-sync python -X utf8 -````
> - Ran `@'
> from pathlib import Path
> import sys,subprocess,tempfile,runpy,frontmatter,contextlib,io
> stage=Path('working/pstack/shared/4_adapt_and_distribute')
> review=frontmatter.load(stage/'replacements.md')
> def call(*args):
>  return subprocess.run([sys.executable,str(stage/'review_input.py'),*args],capture_output=True,text=True)
> p=call('--preview');assert p.returncode==0 and p.stdout.strip()==review['input_id'],(p.stderr,p.stdout)
> p=call('--check-apply');assert p.returncode==1 and 'Missing review input' in p.stderr
> ns=runpy.run_path(str(stage/'review_input.py')); cfg=ns['main'].__globals__
> with tempfile.TemporaryDirectory() as t:
>  root=Path(t);tree=root/'3_autoPR_local_fallback/output'
>  (tree/'agents').mkdir(parents=True);(tree/'skills').mkdir()
>  cfg.update(SHARED=root,ADAPTER=root/'adapter.md',REVIEW=root/'replacements.md')
>  cfg['ADAPTER'].write_text('adapter'); file=tree/'skills/demo.md';file.write_text('a')
>  stamp=ns['input_id'](tree,cfg['ADAPTER'],'stage3')
>  def check(status,key):
>     cfg['REVIEW'].write_text(f'---\nstatus: {status}\ninput_id: {key}\n---\n')
>     sys.argv=['review_input.py','--check-apply']
>     with contextlib.redirect_stderr(io.StringIO()),contextlib.redirect_stdout(io.StringIO()):
>         try: return ns['main']()
>         except SystemExit as e:return e.code
>  assert check('ready-for-human',stamp)==1 and check('done',stamp)==0
>  file.write_text('b');assert check('done',stamp)==1
> print('Verified preview identity, approval, reuse, and invalidation for distribution.')
> '@ | uv run --no-cache --no-sync python -X utf8 -`
> - Ran `@'
> from pathlib import Path
> from markdown_it import MarkdownIt
> import re,frontmatter,subprocess
> base=Path('working/pstack')
> stage=base/'shared/4_adapt_and_distribute'
> for p in [base/'README.md',stage/'requirements.md',stage/'replacements.md']:
>  s=p.read_text(encoding='utf-8')
>  for url in re.findall(r'\]\(([^)]+)\)',s):
>     if not url.startswith(('http:','https:')):assert (p.parent/url).is_file(),(p,url)
> table=frontmatter.load(stage/'replacements.md')
> tokens=MarkdownIt('commonmark').enable('table').parse(table.content)
> print('tables',sum(t.type=='table_open' for t in tokens),'body rows',sum(t.type=='tr_open' for t in tokens)-sum(t.type=='table_open' for t in tokens))
> assert table['status']=='ready-for-human'
> assert all('建议' not in t.content for t in tokens)
> for f in base.rglob('*.md'):
>  if 'output' in f.parts:continue
>  assert not re.search(r'4_cursor_replacement_generalization|5_codex_agent_subdir_complement|forks/(review_input\.py|adaptation-review\.md)',f.read_text(encoding='utf-8')),f
> p=subprocess.run(['git','diff','--check','--','working/pstack'],capture_output=True,text=True);print('diff --check',p.returncode,p.stdout[:160])
> print('Stage 3 output exists:', (base/'shared/3_autoPR_local_fallback/output').exists());print('new distributions exist:',[(f,(base/'forks'/f/'output').exists()) for f in ['generic','codex']])
> '@ | uv run --no-cache --no-sync python -X utf8 -`
>
> </details>
</details>

上一版的“常规映射”是我对上游适配器的二次概括，把本来能直接修改的替换项写成了建议。

我已重写[替换表](./working/pstack/shared/4_adapt_and_distribute/replacements.md)。左栏是实际原文，右栏是预填的最终文字。比如 `~/.cursor/skills/` 对应 `~/.agents/skills/`；同一句编写 skill 的指令，Generic 栏直接写 `Create or edit the skill’s SKILL.md.`，Codex 栏直接写 `Use the skill-creator skill to create or edit SKILL.md.`。你可以直接改右栏。两版相同的只写一次，72 个左栏条目都已在输入文件中逐字核对。

**Stage 4 现在是最后一个 stage，内含两步。** 第一步预填表，由你修改并标记 `done`。第二步在你明确要求分发时，从 Stage 3 直接生成 Generic 和 Codex 两版，同时补齐 Codex 的 `openai.yaml`。[Stage 4 要求](./working/pstack/shared/4_adapt_and_distribute/requirements.md)

目前 Stage 3 还没有产物，表里用的是 Stage 1 原文，状态为 `ready-for-human`。现在就可以改；正式输入生成后会核对差异，保留仍适用的修改。

> ？我问你adaptor指向的文档长啥样，给我链接

[打开 pstack 的 Claude Code 适配器原文 `docs/harness/claude-code.md`](./sources/cursor-plugins/harness/pstack/claude-code/docs/harness/claude-code.md)

文档标题是 **pstack in Claude Code**，主要是 `Cursor` 和 `Claude Code` 两列的对照表。例如：

| Cursor | Claude Code |
| --- | --- |
| `Task` | `Agent` |
| `subagent_type: generalPurpose` | `subagent_type: "general-purpose"` |

<details><summary>1 previous message</summary>

> Context compaction
>
> Source: manual
> Status: completed
</details>

> 你现在写的，回撤然后推倒重来吧，一坨狗屎，看不下去，没法改了。
> shared 4，换成添加codex openai.yaml依赖，然后shared/展平，里面内容拿出来，不再搞
> forks/ 替换为 5_codex_adapt/，里面有两个requirements文档。requirements 5.1，要求上游存在output；step1, 从 # pstack in Claude Code 复制过来一份，改名为cursor-codex； step2，审视上游sources，检查 # pstack in Claude Code 存在哪些遗漏，在最后保持文档风格的追加这些遗漏项；step3，审视上游sources，检查有哪些替换项由于之前的stages，不再需要（比如.agents/约定下，一些路径就不需要再替换了）；step4，把原本 Claude Code 列换成codex，然后对应的工具名直接修改，然后结束等待人类反馈（延续status: ready-for-human/done那一套）。requirements 5.2，确认人类已经完成cursor-codex调整，按照这个文档进行修改，输出到output
>
> 很难吗？我不理解怎么越搞越像一坨大便

<details><summary>2 previous messages</summary>

> 我会撤掉上一版替换表和分发设计，按你给的目录和顺序重写。先核对现有阶段、上游适配器原文，以及哪些内容需要原样保留。这里会用 writing-for-agents 来写给执行 Agent 的 requirements。
>
> <details><summary>Explored a file, ran 36 commands</summary>
>
> - Ran `Get-Location`
>
> <details><summary>Explored 2 files</summary>
>
> - Read `~/.codex/RTK.md`
> - Read `~/.agents/skills/writing-for-agents/SKILL.md`
>
> </details>
>
> - Ran `rg --files --hidden -g 'AGENTS.md' -g '!**/.git/**' -g '!sources/**'`
>
> - Ran `rg --files --hidden working/pstack -g '!**/.git/**' -g '!**/output/**'`
>
> - Ran `git status --short --untracked-files=normal`
>
> - Ran `git status --short --untracked-files=normal --ignore-submodules=all`
>
> - Ran `Get-Content -Raw -Encoding utf8 working/pstack/README.md`
>
> - Ran `git ls-files working/pstack | Select-String -NotMatch '/output/'`
>
> - Ran `rg -n --hidden -g '!**/.git/**' -g '!sources/**' -g '!**/output/**' -g '!releases/**' 'openai\.yaml|pstack/(shared|forks)|4_adapt_and_distribute|5_codex' .`
>
> - Ran `Get-Content -Raw -Encoding utf8 working/pstack/shared/3_autoPR_local_fallback/requirements.md`
>
> - Ran `Get-Content -Raw -Encoding utf8 working/pstack/shared/1_extract_and_pick/extract.py`
>
> - Ran `Get-Content -Raw -Encoding utf8 working/pstack/shared/2_.agent_convention/requirements.md`
>
> - Ran `Get-Content -Raw -Encoding utf8 sources/cursor-plugins/harness/pstack/claude-code/docs/harness/claude-code.md`
>
> - Ran `Get-Content -Raw -Encoding utf8 working/pstack/shared/1_extract_and_pick/requirements.md`
>
> - Ran `Get-Content -Raw -Encoding utf8 working/pstack/forks/generic/dependencies.md`
>
> - Ran `Get-Content -Raw -Encoding utf8 working/pstack/shared/4_adapt_and_distribute/requirements.md`
>
> - Ran `git show HEAD:working/pstack/forks/codex/5_codex_agent_subdir_complement/requirements.md`
>
> - Ran `Get-Content -Raw -Encoding utf8 working/tools/extract_selection.py`
>
> - Ran `Get-ChildItem -Force working/pstack/shared,working/pstack/forks -Depth 2 | Select-Object -ExpandProperty FullName`
>
> - Ran `rg -n --hidden -g '!**/.git/**' -g '!sources/**' -g '!**/output/**' -g '!releases/**' 'shared/|forks/|\.\./\.\./\.\./\.\./sources' .`
>
> - Ran `Get-Command uv`
>
> - Ran `Get-ChildItem -Name sources/cursor-plugins/harness/pstack`
>
> - Ran `Get-Content -Raw -Encoding utf8 AGENTS.md`
>
> - Ran `Get-ChildItem -Name sources/cursor-plugins`
>
> - Ran `Get-ChildItem -Name sources/cursor-plugins/pstack`
>
> - Ran `@'
> from pathlib import Path
>
> pstack = Path("working/pstack").resolve(strict=True)
> assert pstack == Path.cwd().resolve() / "working/pstack"
> shared = pstack / "shared"
> stages = ("1_extract_and_pick", "2_.agent_convention", "3_autoPR_local_fallback")
> old_files = (
>     "shared/4_adapt_and_distribute/requirements.md",
>     "shared/4_adapt_and_distribute/replacements.md",
>     "shared/4_adapt_and_distribute/review_input.py",
>     "forks/generic/dependencies.md",
> )
> for name in stages:
>     src = shared / name
>     dst = pstack / name
>     assert src.resolve(strict=True) == src and src.is_dir()
>     assert dst.resolve() == dst and not dst.exists()
> for name in old_files:
>     path = pstack / name
>     assert path.resolve(strict=True) == path and path.is_file()
> for name in stages:
>     (shared / name).rename(pstack / name)
> for name in old_files:
>     (pstack / name).unlink()
> for name in ("shared/4_adapt_and_distribute", "shared", "forks/generic", "forks/codex", "forks"):
>     (pstack / name).rmdir()
> for name in ("4_codex_openai_yaml", "5_codex_adapt"):
>     (pstack / name).mkdir()
> print("Moved stages 1-3 and removed the superseded distribution files.")
>
> '@ | uv run --no-cache --no-sync python -X utf8 -`
>
> - Ran `@'
> from pathlib import Path
>
> root = (Path.cwd() / "working/pstack").resolve(strict=True)
> assert root == Path.cwd().resolve() / "working/pstack"
> def move(src, dst):
>     assert src.resolve(strict=True) == src and dst.resolve() == dst
>     assert src.is_relative_to(root / "shared") and dst.is_relative_to(root)
>     if dst.exists():
>         raise FileExistsError(dst)
>     try:
>         src.rename(dst)
>     except PermissionError as exc:
>         if exc.winerror != 32 or not src.is_dir():
>             raise
>         dst.mkdir()
>         for child in list(src.iterdir()):
>             move(child, dst / child.name)
>         try:
>             src.rmdir()
>         except PermissionError as err:
>             if err.winerror != 32 or any(src.iterdir()):
>                 raise
>             print("Empty directory held open:", src.relative_to(root))
> for name in ("1_extract_and_pick", "2_.agent_convention", "3_autoPR_local_fallback"):
>     move(root / "shared" / name, root / name)
> for name in ("shared/4_adapt_and_distribute/requirements.md", "shared/4_adapt_and_distribute/replacements.md", "shared/4_adapt_and_distribute/review_input.py", "forks/generic/dependencies.md"):
>     path = root / name
>     assert path.resolve(strict=True) == path
>     path.unlink()
> for name in ("shared/4_adapt_and_distribute", "forks/generic", "forks/codex", "forks", "shared"):
>     path = root / name
>     if not any(path.iterdir()):
>         path.rmdir()
> for name in ("4_codex_openai_yaml", "5_codex_adapt"):
>     (root / name).mkdir()
> print("Stage directories ready.")
>
> '@ | uv run --no-cache --no-sync python -X utf8 -`
>
> - Ran ````$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
> @'
> from pathlib import Path
> root = Path("working/pstack")
> docs = {"README.md":"# pstack 适配流程\n\n| 阶段 | 产物 |\n| --- | --- |\n| [1 · 提取 agents 和 skills](1_extract_and_pick/requirements.md) | 上游的 `agents/` 和 `skills/` |\n| [2 · 统一工作文件路径](2_.agent_convention/requirements.md) | 采用项目路径约定的工作文件 |\n| [3 · 提取 open-a-pr](3_autoPR_local_fallback/requirements.md) | 独立的 `open-a-pr` skill，支持本地合并 |\n| [4 · 添加 Codex openai.yaml](4_codex_openai_yaml/requirements.md) | 为显式调用的 skill 补齐 `agents/openai.yaml` |\n| 5 · 适配 Codex | [5.1 编写 cursor-codex.md，交给人审定](5_codex_adapt/requirements-5.1.md) → [5.2 按定稿生成 output/](5_codex_adapt/requirements-5.2.md) |\n","4_codex_openai_yaml/requirements.md":"# Stage 4 — 添加 Codex 调用策略\n\n复制 `../3_autoPR_local_fallback/output/` 到本阶段的 `output/`。逐个检查 `SKILL.md` 的 frontmatter。含 `disable-model-invocation: true` 且缺少 `agents/openai.yaml` 的 skill，在其目录下创建该文件，内容如下。保留已有的 `agents/openai.yaml`。\n\n```yaml\npolicy:\n  allow_implicit_invocation: false\n```\n","5_codex_adapt/requirements-5.1.md":"# 5.1 编写 cursor-codex.md\n\n开始前确认 `../4_codex_openai_yaml/output/` 已包含上一阶段产出的 `agents/` 和 `skills/`。缺少产物就停在这里。\n\n1. 把上游的 [pstack in Claude Code](../../../sources/cursor-plugins/harness/pstack/claude-code/docs/harness/claude-code.md) 复制到本目录，命名为 `cursor-codex.md`。\n2. 对照[上游 pstack 源码](../../../sources/cursor-plugins/pstack/)核查适配器的遗漏，包括 skill 调用的 playbook 和脚本。把遗漏项按原文的表格或短段落风格追加到文末。\n3. 逐项对照 Stage 4 的实际产物，删去前几个阶段已处理或提取后已用不到的替换项。例如，路径若已在 Stage 2 统一，就删去对应的路径映射。\n4. 将标题改为 `# pstack in Codex`，保留 Cursor 列，把 Claude Code 列改为 Codex。直接填入对应的 Codex 工具名、字段或命令，同步改写表外说明。缺少对应能力时，写明该步骤具体怎么处理。\n\n在文档 frontmatter 中写入 `status: ready-for-human`，然后停止，等人直接编辑并改为 `status: done`。重跑时保留已有人工修改。用 Git 核对自上次审定以来的上游源码和 Stage 4 产物，只更新受变化影响的条目。映射未变时保留原状态。\n","5_codex_adapt/requirements-5.2.md":"# 5.2 按 cursor-codex.md 生成 Codex 产物\n\n收到人的执行指令后，先确认本目录的 `cursor-codex.md` 已由人审定，frontmatter 为 `status: done`。未审定时停止。\n\n以 `../4_codex_openai_yaml/output/` 为底稿，按定稿逐项修改对应的 agent、skill、playbook 和脚本，将完整结果写入本阶段的 `output/`。核对受影响的调用点和文件引用，确保它们使用定稿中的名称、路径和处理方式。\n"}
> for name, content in docs.items():
>     (root / name).write_text(content, encoding="utf-8", newline="\n")
> for name, old, new in (
>     ("1_extract_and_pick/extract.py", "WORKING = STAGE.parents[2]", "WORKING = STAGE.parents[1]"),
>     ("2_.agent_convention/requirements.md", "../../../../sources/", "../../../sources/"),
> ):
>     path = root / name
>     data = path.read_bytes()
>     assert data.count(old.encode()) == 1
>     path.write_bytes(data.replace(old.encode(), new.encode()))
>
> '@ | uv run --no-cache --no-sync python -X utf8 -````
>
> - Ran `@'
> from pathlib import Path
> import re
> root = Path("working/pstack")
> src = Path("sources/cursor-plugins/harness/pstack/claude-code")
> out = root / "1_extract_and_pick/output"
> def snapshot(base):
>     return {p.relative_to(base): p.read_bytes() for sub in ("agents", "skills") for p in (base / sub).rglob("*") if p.is_file()}
> s, o = snapshot(src), snapshot(out)
> assert s == o
> assert {p.name for p in out.iterdir()} == {"agents", "skills"}
> print(len(o), "extracted files match upstream byte for byte")
> docs = [root / "README.md", *root.glob("*/requirements*.md")]
> count = 0
> for f in docs:
>     for href in re.findall(r"\[[^\]]+\]\(([^)]+)\)", f.read_text(encoding="utf-8")):
>         assert (f.parent / href).exists(), (f, href)
>         count += 1
> print(count, "Markdown links resolve across", len(docs), "documents")
> for d in sorted(root.iterdir()):
>     if d.is_dir() and d.name[0].isdigit():
>         print(d.name, "output:", (d / "output").is_dir())
>
> '@ | uv run --no-cache --no-sync python -X utf8 -`
>
> - Ran `rg -n 'shared/|forks/|4_adapt_and_distribute|replacements\.md|review_input\.py|input_id' working/pstack -g '!**/output/**'`
>
> - Ran `@'
> from pathlib import Path
> p = Path.cwd().resolve() / "working/pstack/shared"
> for d in (p/"1_extract_and_pick", p):
>     assert d.resolve() == d
>     if d.exists() and not any(d.iterdir()):
>         try:
>             d.rmdir()
>             print("Removed empty", d.name)
>         except OSError as exc:
>             print(exc)
>
> '@ | uv run --no-cache --no-sync python -X utf8 -`
>
> - Ran `git diff --check -- working/pstack`
>
> - Ran `$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
> @'
> from pathlib import Path
> root = Path("working/pstack")
> p = root / "5_codex_adapt/requirements-5.1.md"
> s = p.read_text(encoding="utf-8")
> s = s.replace("1. 把上游", "1. 首次编写时，把上游").replace("只更新受变化影响的条目。映射未变时保留原状态。", "映射未变就沿用原稿和状态。有变化只更新受影响的条目，交人复审。")
> p.write_text(s, encoding="utf-8", newline="\n")
> p = root / "README.md"
> s = p.read_text(encoding="utf-8").replace("采用项目路径约定的工作文件", "使用项目路径约定的 pstack")
> p.write_text(s, encoding="utf-8", newline="\n")
>
> '@ | uv run --no-cache --no-sync python -X utf8 -`
>
> - Ran `Get-Content -Raw -Encoding utf8 working/pstack/5_codex_adapt/requirements-5.1.md`
>
> - Ran `uv run --no-cache --no-sync python -B working/pstack/1_extract_and_pick/extract.py`
>
> - Ran `Get-ChildItem -Name -Force working/pstack/shared/1_extract_and_pick`
>
> - Ran `@'
> from pathlib import Path
> from ctypes import WinDLL, Structure, byref, c_void_p, c_size_t, c_ulong, c_long, create_string_buffer, sizeof, wintypes
>
> p = Path.cwd().resolve() / "working/pstack/shared/1_extract_and_pick"
> assert p.resolve() == p and not any(p.iterdir())
> try:
>     p.rmdir()
>     p.parent.rmdir()
>     print("Old shared directory removed")
> except PermissionError:
>     kernel = WinDLL("kernel32", use_last_error=True)
>     kernel.CreateFileW.restype = wintypes.HANDLE
>     h = kernel.CreateFileW(str(p), 0x80, 7, None, 3, 0x02000000, None)
>     if h != c_void_p(-1).value:
>         buf = create_string_buffer(8192)
>         iosb = (c_size_t * 2)()
>         status = WinDLL("ntdll").NtQueryInformationFile(c_void_p(h), byref(iosb), buf, sizeof(buf), 47)
>         if status == 0:
>             n = c_ulong.from_buffer(buf).value
>             from os import getpid
>             for pid in (c_size_t * n).from_buffer(buf, sizeof(c_size_t)):
>                 if pid == getpid():
>                     continue
>                 kernel.OpenProcess.restype = wintypes.HANDLE
>                 proc = kernel.OpenProcess(0x1000, False, pid)
>                 if proc:
>                     from ctypes import create_unicode_buffer
>                     name = create_unicode_buffer(1024)
>                     length = c_ulong(len(name))
>                     if kernel.QueryFullProcessImageNameW(c_void_p(proc), 0, name, byref(length)):
>                         print("Open directory handle:", Path(name.value).name)
>                     kernel.CloseHandle(c_void_p(proc))
>         kernel.CloseHandle(c_void_p(h))
>
> '@ | uv run --no-cache --no-sync python -X utf8 -`
>
> </details>
</details>

旧替换表、校验脚本和 `forks/` 已移除。Stage 1–5 现在直接放在 `working/pstack/` 下。

- [Stage 4 requirements](./working/pstack/4_codex_openai_yaml/requirements.md) 给只允许显式调用的 skill 补上缺失的 `agents/openai.yaml`。
- [5.1 requirements](./working/pstack/5_codex_adapt/requirements-5.1.md) 要求先确认 Stage 4 有 `output/`，再复制[上游适配器原文](./sources/cursor-plugins/harness/pstack/claude-code/docs/harness/claude-code.md) 为 `cursor-codex.md`。按原文风格在末尾补遗漏，删掉前序阶段已处理的项，最后把 Claude Code 列改成具体的 Codex 工具、字段或做法，标记 `ready-for-human` 后停下。
- [5.2 requirements](./working/pstack/5_codex_adapt/requirements-5.2.md) 要求人改为 `done` 并发出执行指令后，才按定稿修改 Stage 4 产物，写入 `5_codex_adapt/output/`。

目前 Stage 4 还没有产物，`cursor-codex.md` 尚未生成。迁移后已实际跑通 Stage 1。旧 `shared/1_extract_and_pick/` 是空目录，仍被 Windows 进程占用，无法删除。

> 注意，我让你负责的是requirements的编写，把你生成的替换表给我去了

<details><summary>2 previous messages</summary>

> 我会核对 pstack 工作区和 Git 暂存区，确认上次生成的替换表已移除。`cursor-codex.md` 只作为 requirements 里约定的后续产物。
>
> <details><summary>Ran 4 commands</summary>
>
> - Ran `rg -n --hidden --no-ignore -g '!**/.git/**' -g '!sources/**' -g '!**/output/**' -g '!releases/**' -g '!**/.venv/**' 'ready-for-human|适配器遗漏|替换表|replacements\.md|preview-aec144' working`
> - Ran `rg --files --hidden --no-ignore working/pstack -g '!**/output/**'`
> - Ran `rg --files --hidden -g '!**/.git/**' -g '!sources/**' -g '!**/output/**' -g '!releases/**' | rg -i 'replace|cursor-codex|映射|替换|adaptor|adaptation'`
> - Ran `git ls-files --stage -- working/pstack | Select-String -Pattern 'replacements|cursor-codex|review_input|4_adapt_and_distribute'`
>
> </details>
</details>

我生成的 `replacements.md` 已删除，工作区和 Git 暂存区都已核对。`5_codex_adapt/` 里只有 [5.1 requirements](./working/pstack/5_codex_adapt/requirements-5.1.md) 和 [5.2 requirements](./working/pstack/5_codex_adapt/requirements-5.2.md)。`cursor-codex.md` 留到执行 5.1 时生成。

> 行了，开subagents with fresh context开始执行吧，每个subagent负责一个stage，逐个调用，你只负责orchestrate & observe，比如你注意到某一阶段subagents的执行存在问题，那就停下它，也停下后续流程，向我报告出了什么问题，推荐如何解决

<details><summary>17 previous messages</summary>

> 我会按 Stage 1 到 Stage 5 顺序派发，每次用新的上下文，只给当前阶段所需的路径和要求。每个 Agent 结束后我会核对产物，再决定是否启动下一阶段。发现执行问题就停下报告；到 5.1 的人工审定点也会停下。
>
> Subagent action
>
> Action: spawnAgent
> Status: completed
> Receiver threads: 1
> Prompt: 只执行 pstack Stage 1。仓库 C:/Users/smy/Desktop/agent-workbench。阅读并按 working/pstack/1_extract_and_pick/requirements.md 实际生成该阶段 output/，使用本阶段现有入口，遵循仓库 AGENTS.md（Python 用 uv run）。你的写入范围是本阶段的产物。完成后核对上游，汇报产物路径和验证结果。若执行有问题，立即停止并报告，勿修规格或开始别的阶段。
>
> <details><summary>Ran 4 commands</summary>
>
> - Ran `Get-Content -Encoding utf8 -Raw working/pstack/README.md`
> - Ran `Get-ChildItem -Directory working/pstack | Select-Object -ExpandProperty Name`
> - Ran `rg -n '^#|^\||^Read|^Use|^[0-9]\.' working/pstack/2_.agent_convention/requirements.md working/pstack/3_autoPR_local_fallback/requirements.md`
> - Ran `$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
> @'
> from pathlib import Path
> from hashlib import sha256
> root=Path("working/pstack")
> for f in sorted(root.glob("*/requirements*.md")):
>     print(f.parent.name, f.name, sha256(f.read_bytes()).hexdigest()[:16], "output_exists", (f.parent/"output").exists())
> src=Path("sources/cursor-plugins/harness/pstack/claude-code")
> print("upstream", sum(p.is_file() for name in ("agents","skills") for p in (src/name).rglob("*")), "files")
>
> '@ | uv run --no-cache --no-sync python -B -X utf8 -`
>
> </details>
>
> Subagent action
>
> Action: wait
> Status: completed
> Receiver threads: 1
>
> <details><summary>Ran a command</summary>
>
> - Ran `$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
> @'
> from pathlib import Path
> out = Path("working/pstack/1_extract_and_pick/output")
> src = Path("sources/cursor-plugins/harness/pstack/claude-code")
> assert {p.name for p in out.iterdir()} == {"agents","skills"}
> def snapshot(root):
>     return {p.relative_to(root): p.read_bytes() if p.is_file() else None for top in ("agents","skills") for p in (root/top).rglob("*")}
> a,b=snapshot(out),snapshot(src)
> assert a==b
> print(sum(v is not None for v in a.values()),"matching files")
>
> '@ | uv run --no-cache --no-sync python -B -X utf8 -`
>
> </details>
>
> Subagent action
>
> Action: closeAgent
> Status: completed
> Receiver threads: 1
>
> Stage 1 已通过。提取的 2 个 agent 和 59 个 skill 共 518 个文件，我核对了目录结构和文件内容，均与上游一致。现在交给新的 Agent 执行 Stage 2。
>
> Subagent action
>
> Action: spawnAgent
> Status: completed
> Receiver threads: 1
> Prompt: 只执行 pstack Stage 2，仓库 C:/Users/smy/Desktop/agent-workbench。按 working/pstack/2_.agent_convention/requirements.md 从前一阶段实际 output 生成本阶段完整 output，遵循仓库 AGENTS.md（Python 用 uv run）。以 requirements 为边界，写入仅限本阶段的产物。完成后验证，汇报各工作流改动和验证结果。若执行遇到无法按规格处理的问题，立即停止并报告。不要修订规格或进入别的阶段。
>
> <details><summary>Ran 6 commands</summary>
>
> - Ran `rg -n -i '(decisions?\.tsv|\.audit/|/tmp/.+resume\.md|/tmp/arena-|scratch dir|os\.tmpdir|notes-verify-\$RUN_ID)' working/pstack/1_extract_and_pick/output -g '*.md' -g '!**/test/**'`
> - Ran `Get-Content -Encoding utf8 -Raw working/pstack/1_extract_and_pick/output/skills/poteto-mode/playbooks/opening-a-pr.md`
> - Ran `Get-Content -Encoding utf8 -Raw working/pstack/4_codex_openai_yaml/requirements.md`
> - Ran `rg -n -i 'scratch|tmp|proof|teardown' working/pstack/1_extract_and_pick/output/skills/create-verification-skill -g '*.md'`
> - Ran `rg -n 'open(ing)?[- ]a[- ]pr' -i working/pstack/1_extract_and_pick/output -g '*.md' -g '!**/test/**'`
> - Ran `rg -n -i 'scratch|tmp|outside|--out|render|proof' working/pstack/1_extract_and_pick/output/skills/statechart/SKILL.md working/pstack/1_extract_and_pick/output/skills/ketchup-video/SKILL.md working/pstack/1_extract_and_pick/output/skills/maintain-verification-skill/SKILL.md`
>
> </details>
>
> Subagent action
>
> Action: wait
> Status: completed
> Receiver threads: 0
>
> <details><summary>Ran a command</summary>
>
> - Ran `Get-ChildItem -Force working/pstack/2_.agent_convention | Select-Object Name, LastWriteTime`
>
> </details>
>
> Subagent action
>
> Action: wait
> Status: completed
> Receiver threads: 0
>
> <details><summary>Ran a command</summary>
>
> - Ran `$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
> @'
> from pathlib import Path
> from hashlib import sha256
> root=Path("working/pstack")
> for p in sorted(root.glob("*/output")):
>     print(p.parent.name, sum(f.is_file() for f in p.rglob("*")))
> if (out:=root/"2_.agent_convention/output").exists():
>     inp=root/"1_extract_and_pick/output"
>     for f in sorted(out.rglob("*.md")):
>         base=inp/f.relative_to(out)
>         if not base.exists() or base.read_bytes()!=f.read_bytes():
>             print(f.relative_to(out))
> '@ | uv run --no-cache --no-sync python -B -X utf8 -`
>
> </details>
>
> Subagent action
>
> Action: wait
> Status: completed
> Receiver threads: 0
>
> <details><summary>Ran 9 commands</summary>
>
> - Ran `$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
> @'
> from pathlib import Path
> from hashlib import sha256
> root=Path("working/pstack")
> for p in sorted(root.glob("*/output")):
>     print(p.parent.name, sum(f.is_file() for f in p.rglob("*")))
> if (out:=root/"2_.agent_convention/output").exists():
>     inp=root/"1_extract_and_pick/output"
>     for f in sorted(out.rglob("*.md")):
>         base=inp/f.relative_to(out)
>         if not base.exists() or base.read_bytes()!=f.read_bytes():
>             print(f.relative_to(out))
> '@ | uv run --no-cache --no-sync python -B -X utf8 -`
> - Ran `rg -n '\.agent/|os\.tmpdir|tempfile|gettempdir|PROOF_DIR|NOTES_DATA_DIR|evidence directory' working/pstack/2_.agent_convention/output -g '*.md' -g '!**/test/**'`
> - Ran `Get-Content -Encoding utf8 -TotalCount 31 working/pstack/2_.agent_convention/output/skills/statechart/SKILL.md`
> - Ran `rg -n -i 'default|--out|resolve\(' working/pstack/1_extract_and_pick/output/skills/statechart/scripts/statechart working/pstack/1_extract_and_pick/output/skills/statechart/scripts/src -g '!*.map'`
> - Ran `Get-Content -Encoding utf8 -TotalCount 31 working/pstack/1_extract_and_pick/output/skills/statechart/SKILL.md`
> - Ran `rg -n 'outDir|--out|cwd\(' working/pstack/2_.agent_convention/output/skills/statechart/scripts/statechart.ts`
> - Ran `Get-Content -Encoding utf8 -Raw working/pstack/2_.agent_convention/output/skills/poteto-mode/playbooks/prototype.md`
> - Ran `Get-Content -Encoding utf8 -Raw working/pstack/2_.agent_convention/output/skills/create-verification-skill/references/feature-map-example/README.md`
> - Ran `Get-Content -Encoding utf8 working/pstack/2_.agent_convention/output/skills/statechart/scripts/statechart.ts -TotalCount 50`
>
> </details>
>
> Subagent action
>
> Action: closeAgent
> Status: completed
> Receiver threads: 1
>
> <details><summary>Ran 3 commands</summary>
>
> - Ran `rg -n -- 'Default: SPEC-chart|flags\.out|is not empty' working/pstack/2_.agent_convention/output/skills/statechart/scripts/statechart.ts`
> - Ran `rg -n -- 'Statechart|Create a fresh|Use a new|--out DIR' working/pstack/2_.agent_convention/requirements.md working/pstack/2_.agent_convention/output/skills/statechart/SKILL.md working/pstack/1_extract_and_pick/output/skills/statechart/SKILL.md`
> - Ran `Get-ChildItem -Directory working/pstack | Where-Object { Test-Path (Join-Path $_.FullName 'output') } | Select-Object -ExpandProperty Name`
>
> </details>
</details>

**已停止 Stage 2 的 Agent，Stage 3–5 均未启动。** Stage 1 已通过，518 个文件与上游逐字节一致。

Stage 2 改动了 `statechart` 的输出行为。要求是把临时工作目录改为 `<os.tmpdir>/statechart-<run-id>/`，并尊重调用方传入的 `--out`。Agent 还把调用示例里的 `[--out DIR]` 改成了必填的 `--out DIR`，并指定默认写到 `chart/`。原脚本在省略参数时会按模型名分别写入 `A-chart/`、`B-chart/`。按新说明在同一工作目录检查两个模型，第二次会因 `chart/` 非空而失败。[Stage 2 要求](./working/pstack/2_.agent_convention/requirements.md:13) · [Agent 生成的说明](./working/pstack/2_.agent_convention/output/skills/statechart/SKILL.md:13) · [脚本的默认行为](./working/pstack/2_.agent_convention/output/skills/statechart/scripts/statechart.ts:57)

**建议只修 Stage 2 的这处产物**：保留新的临时工作目录，恢复 `[--out DIR]`，删去固定使用 `chart/` 的指令。当前 Stage 2 产物已留在现场，等待你决定是否继续。

> [$wait-what](C://Users//smy//.agents//skills//wait-what//SKILL.md)

<details><summary>2 previous messages</summary>

> 我会按 `wait-what` 重新说明流程停在哪里，先核对仓库用语。
>
> <details><summary>Ran 3 commands</summary>
>
> - Ran `Get-Content -Encoding utf8 -Raw 'C:/Users/smy/.agents/skills/wait-what/SKILL.md'`
> - Ran `rg --files --hidden -g '!.git' -g '!**/.git/**' -g '!**/.venv/**' -g '!**/node_modules/**' -g 'GLOSSARY.md' -g 'GLOSSARY-MAP.md'`
> - Ran `Get-Content -Encoding utf8 -TotalCount 38 sources/mattpocock-skills/GLOSSARY.md`
>
> </details>
</details>

**Stage 1 passed. I stopped the Stage 2 agent. Stages 3–5 have not started.**

Stage 2 changes where skills keep their work files. For `statechart`, the agent had to put each run in a temporary folder. It also changed the instructions for saving results.

For example, the tool normally saves the results for `A.tla` in `A-chart/` and the results for `B.tla` in `B-chart/`. The new instructions tell the agent to use `chart/` for both. If you check both models in the same run, the second check can fail because `chart/` already contains the first result. I found this by reading the instructions and the script. I did not run the two checks.

**Recommended fix:** Keep the new temporary folder. Remove the instruction to use `chart/`. Let the tool choose the results folder unless the caller gives `--out`. This requires one edit to the [Stage 2 skill instructions](./working/pstack/2_.agent_convention/output/skills/statechart/SKILL.md:13).

> 是requirements写错了，还是agents执行错了，还是未定义？

**是 Stage 2 Agent 执行时多改了一处。**

Requirements 指定了临时工作目录，也要求尊重调用方传入的 `--out`。对于省略 `--out` 的情况，上游脚本已经定义了默认行为：按模型名生成目录，例如 `A-chart/`。这里没有需要 Agent 自行决定的空白。

Agent 在 skill 文档里额外指定了 `chart/`。**建议修 Stage 2 产物，保留新临时目录，恢复可选的 `[--out DIR]`。Requirements 可以原样保留。**

> 把意见返回给对应的subagents修，确认没有问题后，继续后续流程

<details><summary>36 previous messages</summary>

> 我会把具体意见发回原来的 Stage 2 Agent。它修完后，我会核对 `--out` 的默认行为和 Stage 2 的完整产物，再逐阶段继续。
>
> Subagent action
>
> Action: resumeAgent
> Status: completed
> Receiver threads: 1
>
> Subagent action
>
> Action: sendInput
> Status: completed
> Receiver threads: 1
> Prompt: 请在你原来的 Stage 2 产物上修订并完成验证。反馈：statechart 新建 <os.tmpdir>/statechart-<run-id>/ 放 spec/config 是正确的，但 skill 把可选 [--out DIR] 改为 --out DIR，并另定 chart/，改变了上游默认行为。请恢复可选参数，去掉固定 chart/。调用方给 --out 时尊重它，省略时由现有脚本按 spec 名输出。修完对照 Stage 2 requirements 检查整个本阶段产物，再报告修改文件与验证结果。只改本阶段产物，不改 requirements，不启动后续阶段。
>
> <details><summary>Ran 4 commands</summary>
>
> - Ran `Get-Content -Raw -Encoding utf8 working/pstack/5_codex_adapt/requirements-5.1.md`
> - Ran `$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
> @'
> from pathlib import Path
> from difflib import unified_diff
> root=Path("working/pstack")
> inp=root/"1_extract_and_pick/output"
> out=root/"2_.agent_convention/output"
> def paths(base):
>     return {p.relative_to(base) for p in base.rglob("*")}
> a,b=paths(inp),paths(out)
> print("missing",a-b,"additional",b-a)
> for rel in sorted(a & b):
>     f=inp/rel
>     if f.is_file() and f.read_bytes()!=(out/rel).read_bytes():
>         print(rel)
>         if rel.name=="session-pickup.md" or "maintain-verification" in rel.as_posix() or "statechart/" in rel.as_posix():
>             for line in unified_diff(f.read_text(encoding="utf-8").splitlines(), (out/rel).read_text(encoding="utf-8").splitlines(), n=0):
>                 if not line.startswith("---") and not line.startswith("+++") and not line.startswith("@@"):
>                     print(line[:1850])
> '@ | uv run --no-cache --no-sync python -B -X utf8 -`
> - Ran `Get-Content -Raw -Encoding utf8 working/pstack/5_codex_adapt/requirements-5.2.md`
> - Ran `Get-Content -Raw -Encoding utf8 working/pstack/3_autoPR_local_fallback/requirements.md`
>
> </details>
>
> Subagent action
>
> Action: wait
> Status: completed
> Receiver threads: 0
>
> <details><summary>Ran 2 commands</summary>
>
> - Ran `rg -n -- 'Create a fresh|--out DIR|caller|specification' working/pstack/2_.agent_convention/output/skills/statechart/SKILL.md`
> - Ran ``$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
> @'
> from pathlib import Path
> root=Path("working/pstack")
> source=root/"1_extract_and_pick/output"
> out=root/"2_.agent_convention/output"
> def tree(p):
>     return {f.relative_to(p): f.read_bytes() if f.is_file() else None for f in p.rglob("*")}
> a,b=tree(source),tree(out)
> assert a.keys()==b.keys()
> changed=[p for p in a if a[p]!=b[p]]
> assert all(p.suffix==".md" for p in changed)
> expected={
> "arena/SKILL.md":["<os.tmpdir>/arena-<slug>/candidate-<n>/","worktree"],
> "poteto-mode/playbooks/hillclimb.md":[".agent/decision.tsv"],
> "poteto-mode/playbooks/pause-safely.md":["<os.tmpdir>/<slug>-resume.md"],
> "poteto-mode/playbooks/prototype.md":[".agent/prototype/","worktree"],
> "poteto-mode/playbooks/session-pickup.md":[".agent/decisions.tsv",".agent/audit/<task-slug>.tsv"],
> "show-me-your-work/SKILL.md":[".agent/decisions.tsv",".agent/audit/<task-slug>.tsv"],
> "statechart/SKILL.md":["<os.tmpdir>/statechart-<run-id>/","[--out DIR]"],
> "maintain-verification-skill/SKILL.md":[".agent/verify-<app>/<run-id>/"],
> "create-verification-skill/references/feature-map-example/README.md":["<os.tmpdir>/notes-verify-$RUN_ID","PROOF_DIR"],
> "ketchup-video/SKILL.md":["<os.tmpdir>/ketchup-video-<run-id>/"]}
> for name,parts in expected.items():
>     txt=(out/"skills"/name).read_text(encoding="utf-8")
>     for part in parts:
>         assert part in txt,(name,part)
> sc=(out/"skills/statechart/SKILL.md").read_text(encoding="utf-8")
> assert 'new `chart/`' not in sc
> print(sum(x is not None for x in b.values()),'files;',len(changed),'modified Markdown files; eight workflows verified')
>
> '@ | uv run --no-cache --no-sync python -B -X utf8 -``
>
> </details>
>
> Subagent action
>
> Action: wait
> Status: completed
> Receiver threads: 1
>
> Subagent action
>
> Action: closeAgent
> Status: completed
> Receiver threads: 1
>
> Subagent action
>
> Action: spawnAgent
> Status: completed
> Receiver threads: 1
> Prompt: 只执行 pstack Stage 3。仓库 C:/Users/smy/Desktop/agent-workbench。按 working/pstack/3_autoPR_local_fallback/requirements.md，以该文件指定的上阶段实际 output 为输入，在本阶段 output/ 实现并验证全部要求。工作对象是 skill 文件及调用点，无需执行产物中的开 PR、合并等指令。只写本阶段产物，遵循仓库 AGENTS.md，Python 用 uv run。若遇到无法按规格执行的问题，停下并报告。完成后简报改动与验证结果。
>
> 原 Stage 2 Agent 已修正 `statechart`，并用样例实际跑通了省略 `--out`、传相对路径、传绝对路径三种调用。我复核了 518 个文件和八项工作流，Stage 2 通过。Stage 3 已开始提取 `open-a-pr`。
>
> Subagent action
>
> Action: wait
> Status: completed
> Receiver threads: 0
>
> <details><summary>Ran 3 commands</summary>
>
> - Ran `Get-ChildItem -Force working/pstack/3_autoPR_local_fallback | Select-Object -ExpandProperty Name`
> - Ran ``$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
> @'
> from pathlib import Path
> from hashlib import sha256
> from difflib import unified_diff
> root=Path("working/pstack")
> source=root/"2_.agent_convention/output"
> out=root/"3_autoPR_local_fallback/output"
> def tree(base):
>     return {p.relative_to(base): p.read_bytes() for p in base.rglob("*") if p.is_file()}
> a,b=tree(source),tree(out)
> old=Path('skills/poteto-mode/playbooks/opening-a-pr.md')
> new=Path('skills/open-a-pr/SKILL.md')
> assert set(a)-set(b)=={old} and set(b)-set(a)=={new},(set(a)-set(b),set(b)-set(a))
> skill=b[new].decode()
> assert skill.startswith('---') and 'name: open-a-pr' in skill and 'disable-model-invocation: true' in skill and 'description:' in skill
> assert 'Invoked at the end of every other playbook.' not in skill
> assert 'If the repository has no configured Git remote, merge the work branch into the intended local base branch with `git merge` and report the result.' in skill
> assert '[--out DIR]' in b[Path("skills/statechart/SKILL.md")].decode()
> all_changed=[p for p in a.keys() & b.keys() if a[p]!=b[p]]
> print("changed",len(all_changed),"moved playbook; output files",len(b))
> for p in sorted(all_changed):
>     print(str(p))
> for p in b:
>     if p.suffix in {'.md','.py','.sh','.ts','.yml','.yaml'}:
>         assert b'opening-a-pr.md' not in b[p] and b'**Opening a PR**' not in b[p],p
> print(skill)
>
> '@ | uv run --no-cache --no-sync python -B -X utf8 -``
> - Ran `rg -n -i 'open-a-pr|21 playbooks|22 playbooks' working/pstack/3_autoPR_local_fallback/output/skills/poteto-help working/pstack/3_autoPR_local_fallback/output/skills/poteto-mode/SKILL.md`
>
> </details>
>
> Subagent action
>
> Action: wait
> Status: completed
> Receiver threads: 1
>
> Subagent action
>
> Action: closeAgent
> Status: completed
> Receiver threads: 1
>
> Subagent action
>
> Action: spawnAgent
> Status: completed
> Receiver threads: 1
> Prompt: 只执行 pstack Stage 4。仓库 C:/Users/smy/Desktop/agent-workbench。阅读 working/pstack/4_codex_openai_yaml/requirements.md，按其要求从前一阶段完整 output 生成本阶段 output。遵循仓库 AGENTS.md（Python 用 uv run），写入限本阶段 output。核对逐个 skill 的 frontmatter 与 YAML、全部输入文件的保留，简报验证结果。无法按规格执行时停下报告，不启动后续阶段。
>
> <details><summary>Ran 3 commands</summary>
>
> - Ran `Get-Content -Raw -Encoding utf8 working/pstack/4_codex_openai_yaml/requirements.md`
> - Ran `rg -l -i 'agent-transcripts|bugbot|automation.id' working/pstack/3_autoPR_local_fallback/output/skills -g '*.sh' -g '*.py' -g '*.ts' -g '!**/test/**'`
> - Ran `rg -l --fixed-strings '/loop' working/pstack/3_autoPR_local_fallback/output/skills -g '*.md'`
>
> </details>
>
> Subagent action
>
> Action: wait
> Status: completed
> Receiver threads: 1
>
> <details><summary>Ran a command</summary>
>
> - Ran `$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
> @'
> from pathlib import Path
> import re
> root=Path("working/pstack")
> inp=root/"3_autoPR_local_fallback/output"
> out=root/"4_codex_openai_yaml/output"
> def tree(base):
>     return {p.relative_to(base):p.read_bytes() for p in base.rglob("*") if p.is_file()}
> a,b=tree(inp),tree(out)
> targets=set()
> for rel,content in a.items():
>     if rel.name=="SKILL.md":
>         fm=content.decode("utf-8").split("---",2)[1]
>         if re.search(r"(?m)^disable-model-invocation:\s*true\s*$",fm):
>             targets.add(rel.parent/"agents/openai.yaml")
> missing=targets-a.keys()
> assert {p:b[p] for p in a}==a
> assert set(b)-set(a)==missing
> assert all(b[p].decode().splitlines()==["policy:","  allow_implicit_invocation: false"] for p in missing)
> assert Path("skills/open-a-pr/agents/openai.yaml") in b
> print(len(targets),"explicit-only skills;",len(missing),"new YAML files;",len(a),"unchanged input files;",len(b),"total")
>
> '@ | uv run --no-cache --no-sync python -B -X utf8 -`
>
> </details>
>
> Stage 3 和 4 已通过。`open-a-pr` 已独立成 skill，旧 playbook 路径的引用已清零。Stage 4 新增 59 份 `openai.yaml`，其余 518 个文件逐字节一致。现在交给新的 Agent 执行 5.1，下一次交付是供你直接修改的 `cursor-codex.md`。
>
> Subagent action
>
> Action: closeAgent
> Status: completed
> Receiver threads: 1
>
> Subagent action
>
> Action: spawnAgent
> Status: completed
> Receiver threads: 1
> Prompt: 负责 pstack Stage 5，本次只执行 5.1。仓库 C:/Users/smy/Desktop/agent-workbench。读 working/pstack/5_codex_adapt/requirements-5.1.md，按步骤从其指向的上游适配器和 Stage 4 实际产物生成同目录 cursor-codex.md。文档沿用原文简短的英文两列表格与段落风格，目标单元格给出可直接编辑和执行的 Codex 名称或明确做法。核查实际来源、工具能力与缺省行为；已知值得核对的调用点包括 /loop、create-skill、cursor-team-kit、云 worker/pickup、worktree-audit 脚本、watch-pr 的 Bugbot 识别。仅对产物实际涉及者适配。按仓库 AGENTS.md 运行 Python；本次写入仅 cursor-codex.md。完成验证后留 status: ready-for-human，停在人工审定点；不要执行 5.2 或生成 output/。若发生无法按要求执行的问题，停下报告。
>
> <details><summary>Ran 4 commands</summary>
>
> - Ran `rg -n -i 'pinned|active|transcript|delete|dry.run' working/pstack/4_codex_openai_yaml/output/skills/poteto-mode/scripts/worktree-audit.sh working/pstack/4_codex_openai_yaml/output/skills/poteto-mode/playbooks/worktree-cleanup.md`
> - Ran `rg -n -i 'bugbot|automation.?id|actor|reviewer' working/pstack/4_codex_openai_yaml/output/skills/poteto-mode/scripts/watch-pr/github.ts`
> - Ran `Get-Content -Raw -Encoding utf8 sources/cursor-plugins/harness/pstack/claude-code/docs/harness/claude-code.md`
> - Ran `rg -n 'cloud_agent|cloud_base_branch|/loop|/create-skill|cursor-team-kit|control-ui|control-cli' working/pstack/4_codex_openai_yaml/output/skills -g '*.md' -g '!**/test/**' | Select-Object -First 45`
>
> </details>
>
> Subagent action
>
> Action: wait
> Status: completed
> Receiver threads: 0
>
> <details><summary>Ran 3 commands</summary>
>
> - Ran `Get-ChildItem -Force working/pstack/5_codex_adapt | Select-Object -ExpandProperty Name`
> - Ran `rg -l -i 'cursor cli|cursor-agent|cursor://|custom mode|computerUse|ComputerUse|agent.?review|multi.?root|background terminal' working/pstack/4_codex_openai_yaml/output/skills -g '*.md' | Select-Object -First 30`
> - Ran `rg -n '^(#|\|)|cloud_base_branch|resume|isolat|worktree' working/pstack/4_codex_openai_yaml/output/skills/swarm/SKILL.md | Select-Object -First 30`
>
> </details>
>
> Subagent action
>
> Action: wait
> Status: completed
> Receiver threads: 0
>
> <details><summary>Ran 2 commands</summary>
>
> - Ran `$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
> @'
> from pathlib import Path
> from hashlib import sha256
> base=Path("working/pstack")
> for f in sorted(base.glob("*/requirements*.md")):
>     print(f.parent.name, f.name, sha256(f.read_bytes()).hexdigest()[:16])
> last=base/"5_codex_adapt"
> print("5.1 draft exists:",(last/"cursor-codex.md").exists(),"5.2 output exists:",(last/"output").exists())
>
> '@ | uv run --no-cache --no-sync python -B -X utf8 -`
> - Ran `Get-Content -Raw -Encoding utf8 working/pstack/5_codex_adapt/cursor-codex.md`
>
> </details>
>
> Subagent action
>
> Action: wait
> Status: completed
> Receiver threads: 0
>
> Subagent action
>
> Action: wait
> Status: completed
> Receiver threads: 0
>
> <details><summary>Ran 5 commands</summary>
>
> - Ran `rg -n '^(status:|#)' working/pstack/5_codex_adapt/cursor-codex.md`
> - Ran `Get-Content -Raw -Encoding utf8 working/pstack/5_codex_adapt/cursor-codex.md`
> - Ran `rg -n 'file_attachments|/README\.md|docs/harness/claude-code\.md|~/.cursor/rules|\.cursor/rules' working/pstack/4_codex_openai_yaml/output/skills/poteto-help/SKILL.md working/pstack/4_codex_openai_yaml/output/skills -g 'SKILL.md' | Select-Object -First 27`
> - Ran `codex cloud exec --help`
> - Ran `Get-Content -Encoding utf8 working/pstack/4_codex_openai_yaml/output/skills/open-a-pr/SKILL.md`
>
> </details>
>
> Subagent action
>
> Action: sendInput
> Status: completed
> Receiver threads: 1
> Prompt: 我在初稿看到三处会直接影响 5.2 的问题，请在当前 5.1 修好并验证后交付。① 本会话 spawn_agent 的实际 schema 没有 agent_type。generalPurpose 无需传该字段；角色与只读行对支持与不支持该字段的宿主给出可执行做法。② 开头仍要求在运行时按 docs/harness/claude-code.md 读适配器，但包里只有 agents/skills/，5.2 将规则写入文件，请明确替换/移除入口中的旧指针；poteto-help 还有 ../../README.md 和 Claude 安装说明，同上游 guide 一起给出对应去向。③ Stage 3 的 open-a-pr 自己就是“内建 PR 工具”这行映射的调用点，改成 Follow $open-a-pr 会自调用；把目标改成直接执行的 forge 命令，保留 Stage 3 的无 remote 本地合并。每处尽量一行，不增加额外清单。
>
> Subagent action
>
> Action: sendInput
> Status: completed
> Receiver threads: 1
> Prompt: 另请把 worktree-audit.sh 那一行写成能在 5.2 直接改脚本的规则。例如，无可靠的 Codex 聊天数据源时跳过 Cursor transcript 扫描，LAST_CHAT 记 unknown，并在核对 pinned/active 前保留候选 worktree。这样脚本输出和 playbook 的处理一致。
>
> 复核 5.1 初稿时，我发现一条映射会让 `open-a-pr` 调用自己，另一条会让 skill 继续读取产物里不存在的 Claude 适配器。已把这两处连同子代理参数和 worktree 审计脚本的问题发回原 Agent 修订。5.2 仍未启动。
>
> Subagent action
>
> Action: wait
> Status: completed
> Receiver threads: 0
>
> <details><summary>Ran 5 commands</summary>
>
> - Ran `rg -n -i 'stage 5|adapter|agent_type|plugin marketplace|built-in PR tool|LAST_CHAT' working/pstack/5_codex_adapt/cursor-codex.md`
> - Ran `Get-Content -Raw -Encoding utf8 working/pstack/5_codex_adapt/cursor-codex.md`
> - Ran `git diff --check -- working/pstack`
> - Ran `rg -n 'CURSOR_AUTOMATION_ID|RUN_ID|function isBugbot|Math\.max|bugbotReviewPasses' working/pstack/4_codex_openai_yaml/output/skills/poteto-mode/scripts/watch-pr/github.ts`
> - Ran `rg -n -i 'file_attachments|\.cursor/rules(?!/pstack-models)|alwaysApply|/add-plugin|\.cursor/commands' --pcre2 working/pstack/4_codex_openai_yaml/output -g '*.md' -g '!**/test/**'`
>
> </details>
>
> Subagent action
>
> Action: closeAgent
> Status: completed
> Receiver threads: 1
>
> <details><summary>Ran a command</summary>
>
> - Ran ``$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
> @'
> from pathlib import Path
> root=Path("working/pstack/5_codex_adapt")
> assert {p.name for p in root.iterdir()}=={"requirements-5.1.md","requirements-5.2.md","cursor-codex.md"}
> doc=(root/"cursor-codex.md").read_text(encoding="utf-8")
> assert doc.startswith("---\nstatus: ready-for-human\n---\n\n# pstack in Codex\n")
> assert "| Cursor | Claude Code |" not in doc
> for s in ("Remove the entry-point instruction","Omit `agent_type`","git merge <work-branch>","last=unknown","bucket=review","/loop 1h","/create-skill","control-cli","control-ui","codex cloud","CURSOR_AUTOMATION_ID"):
>     assert s in doc,s
> print("Stage 5.1 corrections and status verified; 5.2 output absent.")
>
> '@ | uv run --no-cache --no-sync python -B -X utf8 -``
>
> </details>
</details>

已执行到 **Stage 5.1 的人工审定点**。你可以直接编辑 [cursor-codex.md](./working/pstack/5_codex_adapt/cursor-codex.md)，当前状态是 `ready-for-human`。

- **Stage 2** 由原 Agent 修复了 `statechart`。省略 `--out`、传相对路径、传绝对路径三种调用均已验证通过。
- **Stage 3、4** 已通过。`open-a-pr` 已独立，旧调用已更新。59 个符合条件的 skill 已补上 `openai.yaml`，其余 518 个文件逐字节一致。
- **Stage 5.1** 的复核意见已由原 Agent 修正，包括 `open-a-pr` 自调用、失效的 Claude 适配器链接、Codex 子代理参数，以及 worktree 审计缺少聊天记录时的处理。

5.2 尚未执行。你审定后，把文档状态改为 `done`，再发出执行 5.2 的指令即可。

> [$skill-creator](C://Users//smy//.codex//skills//.system//skill-creator//SKILL.md) 本轮对话，我觉得挺有意思，就是我让agent自己开subagents替我走流程。这种交互模式抽取一个skill

<details><summary>2 previous messages</summary>

> 我会用 `skill-creator` 和 `writing-for-agents` 把这次协作方式写成一个可复用的 skill，重点保留三件事：每阶段用新 Agent、主 Agent 独立验收、出错时由原 Agent 修订。先看仓库里自建 skill 放在哪里。
>
> <details><summary>Ran 23 commands</summary>
>
> - Ran `Get-Content -Raw -Encoding utf8 C:/Users/smy/.codex/skills/.system/skill-creator/SKILL.md`
> - Ran `Get-ChildItem Env:CODEX_HOME -ErrorAction SilentlyContinue`
> - Ran `Get-Content -Raw -Encoding utf8 C:/Users/smy/.codex/RTK.md`
> - Ran `Get-ChildItem -Force -Name`
> - Ran `Get-Content -Raw -Encoding utf8 C:/Users/smy/.agents/skills/writing-for-agents/SKILL.md`
> - Ran `rg --files -g '!sources/**' -g '!**/output/**' -g '!releases/**' -g '!uv.lock' | Select-Object -First 120`
> - Ran `Get-ChildItem -Force -Name sources,working,releases`
> - Ran `Get-Content -Raw -Encoding utf8 C:/Users/smy/.codex/skills/.system/skill-creator/scripts/quick_validate.py`
> - Ran `Get-Content -Raw -Encoding utf8 C:/Users/smy/.agents/skills/writing-for-agents/SKILL-MECHANICS.md`
> - Ran `Get-ChildItem -Directory C:/Users/smy/.codex/skills,C:/Users/smy/.agents/skills | Select-Object -ExpandProperty Name`
> - Ran `Get-Content -Raw -Encoding utf8 pyproject.toml`
> - Ran `Get-ChildItem -Force -Name releases/v0.1.2`
> - Ran `Get-Content -Raw -Encoding utf8 .gitignore`
> - Ran `Get-Content -Raw -Encoding utf8 sources/SOURCES_ETC.md`
> - Ran `Get-ChildItem -Force -Recurse sources/mine,working/mine -Depth 3 | Select-Object -ExpandProperty FullName`
> - Ran `Get-Item -Force C:/Users/smy/.agents/skills/show-me,C:/Users/smy/.codex/skills,C:/Users/smy/Desktop/agent-workbench/sources/mine | Select-Object FullName, LinkType, Target`
> - Ran `Get-Content -Encoding utf8 -TotalCount 26 sources/mine/show-me/SKILL.md`
> - Ran `Get-Content -Encoding utf8 -TotalCount 26 sources/mine/session-review/SKILL.md`
> - Ran `@'
> from pathlib import Path
>
> skill_dir = Path("sources/mine/orchestrate-stages")
> skill_dir.mkdir()
> with (skill_dir / "SKILL.md").open("x", encoding="utf-8", newline="\n") as file:
>     file.write("---\nname: orchestrate-stages\ndescription: Run an existing workflow one stage at a time when the user wants a fresh subagent to own each stage and the main agent to supervise, verify results, and handle handoffs.\n---\n\n# Orchestrate stages\n\nStart at the first stage the user asked to run. Read its requirements and locate its actual input. Keep its steps together under one worker, including any pause for human review. Change requirements only at the user's request.\n\n1. **Dispatch one stage.** Start a fresh subagent without forking the conversation. Give it the stage requirements, input location, permitted output, and any user decision that affects this stage. Ask it to produce the output, verify it, and report what it checked. Keep its agent ID for follow-up.\n2. **Observe and verify.** The worker makes the changes. As coordinator, inspect the actual output yourself. Compare it with the requirements and the input it will replace or pass on. Check a concrete behavior where a change could affect existing callers. For example, if only a scratch path should change, check that omitting an optional argument still gives the original default.\n3. **Handle a discrepancy.** Stop the worker if it is still making the faulty change, and hold later stages. Show the expected behavior, what you observed, and the smallest correction. Identify whether the worker departed from the requirements, the requirements conflict with the user's intent, or a choice needs the user's decision. An existing default usually settles a choice the stage never asked to change.\n4. **Return the correction to its owner.** If the user asked to stop and report, wait for their direction. When a correction is authorized, resume the same worker with the evidence, then independently check its revised output. If the same problem persists, report what is still failing before another attempt.\n5. **Hand off.** After verification passes, give the next fresh subagent the accepted output as its input. At a human review step, link the editable artifact, state what decision is due, and stop. Resume under that stage's stated approval conditions.\n\nReport each handoff briefly. On completion or a stop, identify the last accepted stage, the current artifact, and any work still pending.\n")
>
> '@ | uv run --no-cache --no-sync python -B -X utf8 -`
> - Ran `uv run --no-cache --no-sync python -B -X utf8 C:/Users/smy/.codex/skills/.system/skill-creator/scripts/quick_validate.py sources/mine/orchestrate-stages`
> - Ran `git status --short --untracked-files=all --ignore-submodules=all -- sources/mine/orchestrate-stages`
> - Ran `uv run --no-cache --no-sync python -B -c "import _winapi; print(hasattr(_winapi, 'CreateJunction'))"`
> - Ran `@'
> from pathlib import Path
> import os
> import _winapi
>
> source = Path("C:/Users/smy/Desktop/agent-workbench/sources/mine/orchestrate-stages").resolve(strict=True)
> skills = Path("C:/Users/smy/.codex/skills").resolve(strict=True)
> link = skills / "orchestrate-stages"
> if os.path.lexists(link):
>     if not link.samefile(source):
>         raise FileExistsError(link)
> else:
>     _winapi.CreateJunction(str(source), str(link))
> assert (link / "SKILL.md").samefile(source / "SKILL.md")
> print(link)
>
> '@ | uv run --no-cache --no-sync python -B -X utf8 -`
>
> </details>
</details>

已创建 [`$orchestrate-stages`](./sources/mine/orchestrate-stages/SKILL.md)，已链接到个人 Codex skills 目录并通过格式校验。

它保留了这次协作的分工：**每个 stage 由一个全新上下文的 subagent 执行，主 Agent 负责编排、观察和独立验收。** 发现偏差时暂停后续阶段，说明是执行出错、需求冲突，还是需要人做决定。修订交回原 subagent，验收通过才继续。遇到人工审定点，就交付可编辑文件并停下。

下次可以直接说：

> 用 `$orchestrate-stages` 从 Stage 2 开始跑。发现问题先停下，告诉我原因和建议。
