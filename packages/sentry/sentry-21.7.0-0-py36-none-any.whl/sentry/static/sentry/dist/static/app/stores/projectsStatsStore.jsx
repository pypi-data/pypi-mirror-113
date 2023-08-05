Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var reflux_1 = tslib_1.__importDefault(require("reflux"));
var projectActions_1 = tslib_1.__importDefault(require("app/actions/projectActions"));
/**
 * This is a store specifically used by the dashboard, so that we can
 * clear the store when the Dashboard unmounts
 * (as to not disrupt ProjectsStore which a lot more components use)
 */
var projectsStatsStore = {
    itemsBySlug: {},
    init: function () {
        this.reset();
        this.listenTo(projectActions_1.default.loadStatsForProjectSuccess, this.onStatsLoadSuccess);
        this.listenTo(projectActions_1.default.update, this.onUpdate);
        this.listenTo(projectActions_1.default.updateError, this.onUpdateError);
    },
    getInitialState: function () {
        return this.itemsBySlug;
    },
    reset: function () {
        this.itemsBySlug = {};
        this.updatingItems = new Map();
    },
    onStatsLoadSuccess: function (projects) {
        var _this = this;
        projects.forEach(function (project) {
            _this.itemsBySlug[project.slug] = project;
        });
        this.trigger(this.itemsBySlug);
    },
    /**
     * Optimistic updates
     * @param projectSlug Project slug
     * @param data Project data
     */
    onUpdate: function (projectSlug, data) {
        var _a;
        var project = this.getBySlug(projectSlug);
        this.updatingItems.set(projectSlug, project);
        if (!project) {
            return;
        }
        var newProject = tslib_1.__assign(tslib_1.__assign({}, project), data);
        this.itemsBySlug = tslib_1.__assign(tslib_1.__assign({}, this.itemsBySlug), (_a = {}, _a[project.slug] = newProject, _a));
        this.trigger(this.itemsBySlug);
    },
    onUpdateSuccess: function (data) {
        // Remove project from updating map
        this.updatingItems.delete(data.slug);
    },
    /**
     * Revert project data when there was an error updating project details
     * @param err Error object
     * @param data Previous project data
     */
    onUpdateError: function (_err, projectSlug) {
        var _a;
        var project = this.updatingItems.get(projectSlug);
        if (!project) {
            return;
        }
        this.updatingItems.delete(projectSlug);
        // Restore old project
        this.itemsBySlug = tslib_1.__assign(tslib_1.__assign({}, this.itemsBySlug), (_a = {}, _a[project.slug] = tslib_1.__assign({}, project), _a));
        this.trigger(this.itemsBySlug);
    },
    getAll: function () {
        return this.itemsBySlug;
    },
    getBySlug: function (slug) {
        return this.itemsBySlug[slug];
    },
};
var ProjectsStatsStore = reflux_1.default.createStore(projectsStatsStore);
exports.default = ProjectsStatsStore;
//# sourceMappingURL=projectsStatsStore.jsx.map