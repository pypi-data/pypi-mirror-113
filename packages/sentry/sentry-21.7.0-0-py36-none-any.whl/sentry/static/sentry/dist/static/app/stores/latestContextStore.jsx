Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var reflux_1 = tslib_1.__importDefault(require("reflux"));
var navigationActions_1 = tslib_1.__importDefault(require("app/actions/navigationActions"));
var organizationActions_1 = tslib_1.__importDefault(require("app/actions/organizationActions"));
var organizationsActions_1 = tslib_1.__importDefault(require("app/actions/organizationsActions"));
var projectActions_1 = tslib_1.__importDefault(require("app/actions/projectActions"));
// Keeps track of last usable project/org
// this currently won't track when users navigate out of a org/project completely,
// it tracks only if a user switches into a new org/project
//
// Only keep slug so that people don't get the idea to access org/project data here
// Org/project data is currently in organizationsStore/projectsStore
var storeConfig = {
    state: {
        project: null,
        lastProject: null,
        organization: null,
        environment: null,
        lastRoute: null,
    },
    getInitialState: function () {
        return this.state;
    },
    init: function () {
        this.reset();
        this.listenTo(projectActions_1.default.setActive, this.onSetActiveProject);
        this.listenTo(projectActions_1.default.updateSuccess, this.onUpdateProject);
        this.listenTo(organizationsActions_1.default.setActive, this.onSetActiveOrganization);
        this.listenTo(organizationsActions_1.default.update, this.onUpdateOrganization);
        this.listenTo(organizationActions_1.default.update, this.onUpdateOrganization);
        this.listenTo(navigationActions_1.default.setLastRoute, this.onSetLastRoute);
    },
    reset: function () {
        this.state = {
            project: null,
            lastProject: null,
            organization: null,
            environment: null,
            lastRoute: null,
        };
        return this.state;
    },
    onSetLastRoute: function (route) {
        this.state = tslib_1.__assign(tslib_1.__assign({}, this.state), { lastRoute: route });
        this.trigger(this.state);
    },
    onUpdateOrganization: function (org) {
        // Don't do anything if base/target orgs are falsey
        if (!this.state.organization) {
            return;
        }
        if (!org) {
            return;
        }
        // Check to make sure current active org is what has been updated
        if (org.slug !== this.state.organization.slug) {
            return;
        }
        this.state = tslib_1.__assign(tslib_1.__assign({}, this.state), { organization: org });
        this.trigger(this.state);
    },
    onSetActiveOrganization: function (org) {
        if (!org) {
            this.state = tslib_1.__assign(tslib_1.__assign({}, this.state), { organization: null, project: null });
        }
        else if (!this.state.organization || this.state.organization.slug !== org.slug) {
            // Update only if different
            this.state = tslib_1.__assign(tslib_1.__assign({}, this.state), { organization: org, project: null });
        }
        this.trigger(this.state);
    },
    onSetActiveProject: function (project) {
        if (!project) {
            this.state = tslib_1.__assign(tslib_1.__assign({}, this.state), { lastProject: this.state.project, project: null });
        }
        else if (!this.state.project || this.state.project.slug !== project.slug) {
            // Update only if different
            this.state = tslib_1.__assign(tslib_1.__assign({}, this.state), { lastProject: this.state.project, project: project });
        }
        this.trigger(this.state);
    },
    onUpdateProject: function (project) {
        this.state = tslib_1.__assign(tslib_1.__assign({}, this.state), { project: project });
        this.trigger(this.state);
    },
};
var LatestContextStore = reflux_1.default.createStore(storeConfig);
exports.default = LatestContextStore;
//# sourceMappingURL=latestContextStore.jsx.map