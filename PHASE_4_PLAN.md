# Phase 4: Database Integration - Complete Plan

**Timeline**: ~2-3 hours  
**Objective**: Replace in-memory session store with PostgreSQL persistence layer

---

## 📋 Phase 4 Overview

### Current State (Phase 3)
- All data stored in-memory (session_store dictionary)
- Session data lost on server restart
- No multi-user support
- No data persistence/analytics

### Target State (Phase 4)
- PostgreSQL database for persistent storage
- SQLAlchemy ORM for type-safe queries
- pgvector for skill embeddings/semantic search
- Session management with history tracking
- Ready for multi-user deployment

---

## 🎯 Phase 4 Tasks Breakdown

### Task 1: Database Design & Schema (20 min)
**Objective**: Design database schema for persistent storage

**Tables to Create**:
1. **users**
   - id (UUID primary key)
   - email (unique)
   - name
   - created_at
   - updated_at

2. **sessions**
   - id (UUID primary key)
   - user_id (foreign key)
   - skill_assessed (string)
   - status (active/completed)
   - created_at
   - updated_at

3. **assessments**
   - id (UUID primary key)
   - session_id (foreign key)
   - jd_text (text)
   - resume_text (text)
   - jd_skills (array of strings)
   - resume_skills (array of strings)
   - created_at

4. **skill_scores**
   - id (UUID primary key)
   - session_id (foreign key)
   - skill (string)
   - proficiency_level (1-5)
   - confidence (0-100)
   - gap_from_required (integer)
   - created_at

5. **conversation_histories**
   - id (UUID primary key)
   - session_id (foreign key)
   - skill (string)
   - turn_count (integer)
   - question (text)
   - response (text)
   - response_quality (0-1)
   - created_at

6. **learning_plans**
   - id (UUID primary key)
   - session_id (foreign key)
   - skill (string)
   - gap_level (integer)
   - recommended_actions (array of strings)
   - estimated_hours (integer)
   - created_at

---

### Task 2: SQLAlchemy Models (30 min)
**Objective**: Create ORM models for database tables

**Files to Create**:
- `backend/app/models/user.py` - User model
- `backend/app/models/session.py` - Session model
- `backend/app/models/assessment.py` - Assessment model
- `backend/app/models/skill_score.py` - Skill score model
- `backend/app/models/conversation.py` - Conversation history model
- `backend/app/models/learning_plan.py` - Learning plan model
- `backend/app/models/base.py` - Base model with common fields
- `backend/app/models/__init__.py` - Model exports

**Key Features**:
- UUID primary keys
- Timestamps (created_at, updated_at)
- Foreign key relationships
- Indexes on frequently queried fields
- Cascading deletes where appropriate

---

### Task 3: Database Configuration (20 min)
**Objective**: Set up database connection and session management

**Files to Create**:
- `backend/app/db/database.py` - Database connection
- `backend/app/db/session.py` - Session factory
- `backend/app/db/init_db.py` - Database initialization

**Key Features**:
- SQLAlchemy connection pooling
- Environment variable for DATABASE_URL
- Async session support
- Migration-ready structure

---

### Task 4: Database Migrations (Alembic) (20 min)
**Objective**: Set up schema versioning and migrations

**Steps**:
1. Initialize Alembic: `alembic init alembic`
2. Configure alembic.ini for PostgreSQL
3. Create initial migration
4. Document migration process

---

### Task 5: Repository/DAO Layer (40 min)
**Objective**: Create data access layer to replace session_store

**Files to Create**:
- `backend/app/repositories/base.py` - Base repository
- `backend/app/repositories/user_repo.py` - User operations
- `backend/app/repositories/session_repo.py` - Session operations
- `backend/app/repositories/assessment_repo.py` - Assessment operations
- `backend/app/repositories/skill_score_repo.py` - Skill score operations
- `backend/app/repositories/conversation_repo.py` - Conversation operations
- `backend/app/repositories/learning_plan_repo.py` - Learning plan operations

**Key Methods**:
- `create()` - Insert new record
- `get()` - Fetch by ID
- `get_all()` - List all records
- `update()` - Modify record
- `delete()` - Remove record
- `get_by_session()` - Fetch records for a session

---

### Task 6: Update Main.py (30 min)
**Objective**: Replace in-memory session_store with database

**Changes**:
1. Remove session_store dictionary
2. Replace with database calls via repositories
3. Add dependency injection for repositories
4. Update all endpoints to use database

**Endpoints to Update**:
- `/api/v1/upload` - Save assessment
- `/api/v1/chat` - Save conversation
- `/api/v1/score` - Save skill scores
- `/api/v1/plan` - Save learning plan
- `/api/v1/gaps` - Query skill gaps (now from DB)

---

### Task 7: Update Agents (20 min)
**Objective**: Add database logging to AI agents

**Changes**:
1. AssessmentAgent - Log conversations to DB
2. ScoringAgent - Save proficiency scores
3. GapAnalysisAgent - Save identified gaps
4. PlanningAgent - Save learning recommendations

---

### Task 8: Create Database Tests (30 min)
**Objective**: Test database integration

**Files to Create**:
- `test_phase4_database.py` - Database integration tests

**Test Cases**:
- User CRUD operations
- Session management
- Conversation history tracking
- Skill score persistence
- Gap analysis persistence
- Learning plan retrieval

---

### Task 9: Update Integration Tests (15 min)
**Objective**: Update Phase 2.5 tests to work with database

**Changes**:
- Update `test_phase25_integration.py` to use database
- Add database cleanup between tests
- Verify data persistence across calls

---

### Task 10: Documentation (15 min)
**Objective**: Document Phase 4 changes

**Files to Create**:
- `PHASE_4_DATABASE.md` - Database implementation guide
- `PHASE_4_QUICK_REFERENCE.md` - Quick lookup
- `PHASE_4_MIGRATION_GUIDE.md` - How to run migrations
- `PHASE_4_COMPLETE.md` - Completion summary

---

## 📊 Implementation Order

```
1. Task 1: Database Design (20 min)
   ↓
2. Task 2: SQLAlchemy Models (30 min)
   ↓
3. Task 3: Database Configuration (20 min)
   ↓
4. Task 4: Alembic Migrations (20 min)
   ↓
5. Task 5: Repository Layer (40 min)
   ↓
6. Task 6: Update Main.py (30 min)
   ↓
7. Task 7: Update Agents (20 min)
   ↓
8. Task 8: Database Tests (30 min)
   ↓
9. Task 9: Integration Tests (15 min)
   ↓
10. Task 10: Documentation (15 min)
```

**Total Estimated Time**: 2.5-3 hours

---

## 🛠️ Technology Stack

| Component | Package | Version | Purpose |
|-----------|---------|---------|---------|
| Database | PostgreSQL | 15+ | Data persistence |
| ORM | SQLAlchemy | 2.0+ | Object-relational mapping |
| Migrations | Alembic | 1.12+ | Schema versioning |
| Vector DB | pgvector | 0.5+ | Semantic search (Phase 4.5) |
| Async Driver | asyncpg | 0.29+ | Async PostgreSQL driver |

---

## 📋 Dependencies to Install

```bash
pip install sqlalchemy==2.0.23
pip install alembic==1.12.1
pip install asyncpg==0.29.0
pip install psycopg2-binary==2.9.9
pip install pgvector==0.2.0
```

---

## 🚀 Getting Started

### Step 1: Set up PostgreSQL
```bash
# Install PostgreSQL (if not already installed)
# macOS:
brew install postgresql

# Start PostgreSQL
brew services start postgresql

# Create database
createdb hackathon_deccan_db
```

### Step 2: Environment Setup
```bash
# Create .env file in backend/
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/hackathon_deccan_db
ENVIRONMENT=development
```

### Step 3: Initialize Database
```bash
# Install dependencies
pip install -r backend/requirements-phase4.txt

# Create tables
cd backend
python3 -m alembic upgrade head
```

### Step 4: Run Tests
```bash
# Test database operations
python3 test_phase4_database.py

# Test full integration
python3 test_phase25_integration.py
```

---

## ✅ Success Criteria

- [ ] PostgreSQL database created and accessible
- [ ] All SQLAlchemy models defined and validated
- [ ] Migration system working (Alembic)
- [ ] Repository layer fully implemented
- [ ] main.py using database instead of session_store
- [ ] All Phase 2.5 tests passing with database
- [ ] Phase 4 tests 100% passing
- [ ] Documentation complete
- [ ] No breaking changes to existing API

---

## 📊 Expected Outcomes

### After Phase 4 Completion:
- ✅ Persistent data storage
- ✅ Multi-user session support
- ✅ Assessment history tracking
- ✅ Analytics capability (skill trends, etc.)
- ✅ Data export/reporting ready
- ✅ Production-ready persistence layer

### Before Phase 5:
- ✅ Database fully operational
- ✅ Data migration tools ready
- ✅ Backup/restore procedures defined
- ✅ Performance optimized (indexes, queries)

---

## 🔄 Rollback Plan

If issues occur:
1. Alembic provides downgrade: `alembic downgrade -1`
2. Keep session_store code as fallback (disabled but present)
3. Document any data recovery procedures

---

## 📞 Next Steps After Phase 4

Once Phase 4 completes:
1. ✅ Database persistence working
2. ✅ Ready for Phase 5 (Frontend)
3. ✅ Ready for production deployment
4. ✅ Analytics dashboard preparation

---

**Status**: Ready to begin Phase 4 implementation  
**Start Time**: April 26, 2026  
**Estimated Completion**: April 26, 2026 (2.5-3 hours)
