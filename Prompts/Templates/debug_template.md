# Debug Task - {project_name}

**Generated**: {timestamp}  
**Stage**: {current_stage}  
**Root Path**: {project_root}

## 🐛 Issue Description
{issue_description}

## ❌ Error Details
{error_details}

## 📋 Current Context
{context}

## 🔄 Reproduction Steps
{reproduction_steps}

## 🔍 Investigation Areas
{investigation_areas}

## 🛠️ Debug Guidelines

### Systematic Approach
1. **Reproduce the issue** - Confirm you can recreate the problem
2. **Check recent changes** - Review git log for recent modifications
3. **Examine logs** - Check all relevant log files in `Logs/`
4. **Add debug logging** - Insert temporary debug statements
5. **Test hypotheses** - Systematically test potential causes
6. **Verify fix** - Ensure the fix resolves the issue without side effects

### Debug Tools
- Use Python debugger: `import pdb; pdb.set_trace()`
- Add verbose logging: `logger.debug(f"Variable state: {var}")`
- Use print statements for quick checks
- Check system resources (memory, disk, CPU)
- Validate input data formats

## 📁 Files to Check
{files_to_check}

## 🔬 Common Issues to Check
- [ ] Environment variables properly loaded from .env
- [ ] File paths are correct and exist
- [ ] API keys/tokens are valid and not expired
- [ ] Network connectivity for external services
- [ ] Proper error handling in try-except blocks
- [ ] Correct data types and formats
- [ ] Race conditions or timing issues
- [ ] Resource exhaustion (memory, file handles)

## ✅ Resolution Criteria
{resolution_criteria}

## 🧪 Testing After Fix
1. **Verify fix works** - Test the specific issue is resolved
2. **Regression testing** - Ensure no new issues introduced
3. **Edge cases** - Test boundary conditions
4. **Performance** - Check if fix impacts performance
5. **Documentation** - Update docs if behavior changed

## 📝 Fix Documentation
Once resolved, document:
- Root cause of the issue
- Solution implemented
- Any workarounds if applicable
- Preventive measures for future

## 🔄 Post-Debug Checklist
- [ ] Issue reproduced and understood
- [ ] Root cause identified
- [ ] Fix implemented and tested
- [ ] No regression in other features
- [ ] Tests updated/added for this case
- [ ] CHANGELOG.md updated
- [ ] Debug code removed (no leftover print/pdb)
- [ ] Commit with clear fix description
- [ ] Copy debug report to Update_AI/

---
**Remember**: Document your findings for future reference.
