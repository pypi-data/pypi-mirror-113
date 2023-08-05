Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var reflux_1 = tslib_1.__importDefault(require("reflux"));
var projectActions_1 = tslib_1.__importDefault(require("app/actions/projectActions"));
var teamActions_1 = tslib_1.__importDefault(require("app/actions/teamActions"));
var storeConfig = {
    itemsById: {},
    loading: true,
    init: function () {
        this.reset();
        this.listenTo(projectActions_1.default.addTeamSuccess, this.onAddTeam);
        this.listenTo(projectActions_1.default.changeSlug, this.onChangeSlug);
        this.listenTo(projectActions_1.default.createSuccess, this.onCreateSuccess);
        this.listenTo(projectActions_1.default.loadProjects, this.loadInitialData);
        this.listenTo(projectActions_1.default.loadStatsSuccess, this.onStatsLoadSuccess);
        this.listenTo(projectActions_1.default.removeTeamSuccess, this.onRemoveTeam);
        this.listenTo(projectActions_1.default.reset, this.reset);
        this.listenTo(projectActions_1.default.updateSuccess, this.onUpdateSuccess);
        this.listenTo(teamActions_1.default.removeTeamSuccess, this.onDeleteTeam);
    },
    reset: function () {
        this.itemsById = {};
        this.loading = true;
    },
    loadInitialData: function (items) {
        this.itemsById = items.reduce(function (map, project) {
            map[project.id] = project;
            return map;
        }, {});
        this.loading = false;
        this.trigger(new Set(Object.keys(this.itemsById)));
    },
    onChangeSlug: function (prevSlug, newSlug) {
        var _a;
        var prevProject = this.getBySlug(prevSlug);
        // This shouldn't happen
        if (!prevProject) {
            return;
        }
        var newProject = tslib_1.__assign(tslib_1.__assign({}, prevProject), { slug: newSlug });
        this.itemsById = tslib_1.__assign(tslib_1.__assign({}, this.itemsById), (_a = {}, _a[newProject.id] = newProject, _a));
        // Ideally we'd always trigger this.itemsById, but following existing patterns
        // so we don't break things
        this.trigger(new Set([prevProject.id]));
    },
    onCreateSuccess: function (project) {
        var _a;
        this.itemsById = tslib_1.__assign(tslib_1.__assign({}, this.itemsById), (_a = {}, _a[project.id] = project, _a));
        this.trigger(new Set([project.id]));
    },
    onUpdateSuccess: function (data) {
        var _a;
        var project = this.getById(data.id);
        if (!project) {
            return;
        }
        var newProject = Object.assign({}, project, data);
        this.itemsById = tslib_1.__assign(tslib_1.__assign({}, this.itemsById), (_a = {}, _a[project.id] = newProject, _a));
        this.trigger(new Set([data.id]));
    },
    onStatsLoadSuccess: function (data) {
        var _this = this;
        var touchedIds = [];
        Object.entries(data || {}).forEach(function (_a) {
            var _b = tslib_1.__read(_a, 2), projectId = _b[0], stats = _b[1];
            if (projectId in _this.itemsById) {
                _this.itemsById[projectId].stats = stats;
                touchedIds.push(projectId);
            }
        });
        this.trigger(new Set(touchedIds));
    },
    /**
     * Listener for when a team is completely removed
     *
     * @param teamSlug Team Slug
     */
    onDeleteTeam: function (teamSlug) {
        var _this = this;
        // Look for team in all projects
        var projectIds = this.getWithTeam(teamSlug).map(function (projectWithTeam) {
            _this.removeTeamFromProject(teamSlug, projectWithTeam);
            return projectWithTeam.id;
        });
        this.trigger(new Set([projectIds]));
    },
    onRemoveTeam: function (teamSlug, projectSlug) {
        var project = this.getBySlug(projectSlug);
        if (!project) {
            return;
        }
        this.removeTeamFromProject(teamSlug, project);
        this.trigger(new Set([project.id]));
    },
    onAddTeam: function (team, projectSlug) {
        var _a;
        var project = this.getBySlug(projectSlug);
        // Don't do anything if we can't find a project
        if (!project) {
            return;
        }
        this.itemsById = tslib_1.__assign(tslib_1.__assign({}, this.itemsById), (_a = {}, _a[project.id] = tslib_1.__assign(tslib_1.__assign({}, project), { teams: tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(project.teams)), [team]) }), _a));
        this.trigger(new Set([project.id]));
    },
    // Internal method, does not trigger
    removeTeamFromProject: function (teamSlug, project) {
        var _a;
        var newTeams = project.teams.filter(function (_a) {
            var slug = _a.slug;
            return slug !== teamSlug;
        });
        this.itemsById = tslib_1.__assign(tslib_1.__assign({}, this.itemsById), (_a = {}, _a[project.id] = tslib_1.__assign(tslib_1.__assign({}, project), { teams: newTeams }), _a));
    },
    /**
     * Returns a list of projects that has the specified team
     *
     * @param {String} teamSlug Slug of team to find in projects
     */
    getWithTeam: function (teamSlug) {
        return this.getAll().filter(function (_a) {
            var teams = _a.teams;
            return teams.find(function (_a) {
                var slug = _a.slug;
                return slug === teamSlug;
            });
        });
    },
    getAll: function () {
        return Object.values(this.itemsById).sort(function (a, b) {
            if (a.slug > b.slug) {
                return 1;
            }
            if (a.slug < b.slug) {
                return -1;
            }
            return 0;
        });
    },
    getById: function (id) {
        return this.getAll().find(function (project) { return project.id === id; });
    },
    getBySlug: function (slug) {
        return this.getAll().find(function (project) { return project.slug === slug; });
    },
    getBySlugs: function (slugs) {
        return this.getAll().filter(function (project) { return slugs.includes(project.slug); });
    },
    getState: function (slugs) {
        return {
            projects: slugs ? this.getBySlugs(slugs) : this.getAll(),
            loading: this.loading,
        };
    },
};
var ProjectsStore = reflux_1.default.createStore(storeConfig);
exports.default = ProjectsStore;
//# sourceMappingURL=projectsStore.jsx.map