Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var reflux_1 = tslib_1.__importDefault(require("reflux"));
var organizationActions_1 = tslib_1.__importDefault(require("app/actions/organizationActions"));
var projectActions_1 = tslib_1.__importDefault(require("app/actions/projectActions"));
var teamActions_1 = tslib_1.__importDefault(require("app/actions/teamActions"));
var constants_1 = require("app/constants");
var storeConfig = {
    init: function () {
        this.reset();
        this.listenTo(organizationActions_1.default.update, this.onUpdate);
        this.listenTo(organizationActions_1.default.fetchOrg, this.reset);
        this.listenTo(organizationActions_1.default.fetchOrgError, this.onFetchOrgError);
        // fill in teams and projects if they are loaded
        this.listenTo(projectActions_1.default.loadProjects, this.onLoadProjects);
        this.listenTo(teamActions_1.default.loadTeams, this.onLoadTeams);
        // mark the store as dirty if projects or teams change
        this.listenTo(projectActions_1.default.createSuccess, this.onProjectOrTeamChange);
        this.listenTo(projectActions_1.default.updateSuccess, this.onProjectOrTeamChange);
        this.listenTo(projectActions_1.default.changeSlug, this.onProjectOrTeamChange);
        this.listenTo(projectActions_1.default.addTeamSuccess, this.onProjectOrTeamChange);
        this.listenTo(projectActions_1.default.removeTeamSuccess, this.onProjectOrTeamChange);
        this.listenTo(teamActions_1.default.updateSuccess, this.onProjectOrTeamChange);
        this.listenTo(teamActions_1.default.removeTeamSuccess, this.onProjectOrTeamChange);
        this.listenTo(teamActions_1.default.createTeamSuccess, this.onProjectOrTeamChange);
    },
    reset: function () {
        this.loading = true;
        this.error = null;
        this.errorType = null;
        this.organization = null;
        this.dirty = false;
        this.trigger(this.get());
    },
    onUpdate: function (updatedOrg, _a) {
        var _b = _a === void 0 ? {} : _a, _c = _b.replace, replace = _c === void 0 ? false : _c;
        this.loading = false;
        this.error = null;
        this.errorType = null;
        this.organization = replace ? updatedOrg : tslib_1.__assign(tslib_1.__assign({}, this.organization), updatedOrg);
        this.dirty = false;
        this.trigger(this.get());
    },
    onFetchOrgError: function (err) {
        this.organization = null;
        this.errorType = null;
        switch (err === null || err === void 0 ? void 0 : err.status) {
            case 401:
                this.errorType = constants_1.ORGANIZATION_FETCH_ERROR_TYPES.ORG_NO_ACCESS;
                break;
            case 404:
                this.errorType = constants_1.ORGANIZATION_FETCH_ERROR_TYPES.ORG_NOT_FOUND;
                break;
            default:
        }
        this.loading = false;
        this.error = err;
        this.dirty = false;
        this.trigger(this.get());
    },
    onProjectOrTeamChange: function () {
        // mark the store as dirty so the next fetch will trigger an org details refetch
        this.dirty = true;
    },
    onLoadProjects: function (projects) {
        if (this.organization) {
            // sort projects to mimic how they are received from backend
            projects.sort(function (a, b) { return a.slug.localeCompare(b.slug); });
            this.organization = tslib_1.__assign(tslib_1.__assign({}, this.organization), { projects: projects });
            this.trigger(this.get());
        }
    },
    onLoadTeams: function (teams) {
        if (this.organization) {
            // sort teams to mimic how they are received from backend
            teams.sort(function (a, b) { return a.slug.localeCompare(b.slug); });
            this.organization = tslib_1.__assign(tslib_1.__assign({}, this.organization), { teams: teams });
            this.trigger(this.get());
        }
    },
    get: function () {
        return {
            organization: this.organization,
            error: this.error,
            loading: this.loading,
            errorType: this.errorType,
            dirty: this.dirty,
        };
    },
};
var OrganizationStore = reflux_1.default.createStore(storeConfig);
exports.default = OrganizationStore;
//# sourceMappingURL=organizationStore.jsx.map