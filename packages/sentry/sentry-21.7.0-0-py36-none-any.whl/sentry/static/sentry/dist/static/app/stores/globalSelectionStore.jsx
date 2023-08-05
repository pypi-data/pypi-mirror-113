Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var reflux_1 = tslib_1.__importDefault(require("reflux"));
var globalSelectionActions_1 = tslib_1.__importDefault(require("app/actions/globalSelectionActions"));
var utils_1 = require("app/components/organizations/globalSelectionHeader/utils");
var globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
var organizationsStore_1 = tslib_1.__importDefault(require("app/stores/organizationsStore"));
var isEqualWithDates_1 = require("app/utils/isEqualWithDates");
var localStorage_1 = tslib_1.__importDefault(require("app/utils/localStorage"));
var storeConfig = {
    state: utils_1.getDefaultSelection(),
    init: function () {
        this.reset(this.state);
        this.listenTo(globalSelectionActions_1.default.reset, this.onReset);
        this.listenTo(globalSelectionActions_1.default.initializeUrlState, this.onInitializeUrlState);
        this.listenTo(globalSelectionActions_1.default.setOrganization, this.onSetOrganization);
        this.listenTo(globalSelectionActions_1.default.save, this.onSave);
        this.listenTo(globalSelectionActions_1.default.updateProjects, this.updateProjects);
        this.listenTo(globalSelectionActions_1.default.updateDateTime, this.updateDateTime);
        this.listenTo(globalSelectionActions_1.default.updateEnvironments, this.updateEnvironments);
    },
    reset: function (state) {
        // Has passed the enforcement state
        this._hasEnforcedProject = false;
        this._hasInitialState = false;
        this.state = state || utils_1.getDefaultSelection();
    },
    isReady: function () {
        return this._hasInitialState;
    },
    onSetOrganization: function (organization) {
        this.organization = organization;
    },
    /**
     * Initializes the global selection store data
     */
    onInitializeUrlState: function (newSelection) {
        this._hasInitialState = true;
        this.state = newSelection;
        this.trigger(this.get());
    },
    get: function () {
        return {
            selection: this.state,
            isReady: this.isReady(),
        };
    },
    onReset: function () {
        this.reset();
        this.trigger(this.get());
    },
    updateProjects: function (projects, environments) {
        if (projects === void 0) { projects = []; }
        if (environments === void 0) { environments = null; }
        if (isEqual_1.default(this.state.projects, projects)) {
            return;
        }
        this.state = tslib_1.__assign(tslib_1.__assign({}, this.state), { projects: projects, environments: environments === null ? this.state.environments : environments });
        this.trigger(this.get());
    },
    updateDateTime: function (datetime) {
        if (isEqualWithDates_1.isEqualWithDates(this.state.datetime, datetime)) {
            return;
        }
        this.state = tslib_1.__assign(tslib_1.__assign({}, this.state), { datetime: datetime });
        this.trigger(this.get());
    },
    updateEnvironments: function (environments) {
        if (isEqual_1.default(this.state.environments, environments)) {
            return;
        }
        this.state = tslib_1.__assign(tslib_1.__assign({}, this.state), { environments: environments !== null && environments !== void 0 ? environments : [] });
        this.trigger(this.get());
    },
    /**
     * Save to local storage when user explicitly changes header values.
     *
     * e.g. if localstorage is empty, user loads issue details for project "foo"
     * this should not consider "foo" as last used and should not save to local storage.
     *
     * However, if user then changes environment, it should...? Currently it will
     * save the current project alongside environment to local storage. It's debatable if
     * this is the desired behavior.
     */
    onSave: function (updateObj) {
        // Do nothing if no org is loaded or user is not an org member. Only
        // organizations that a user has membership in will be available via the
        // organizations store
        if (!this.organization || !organizationsStore_1.default.get(this.organization.slug)) {
            return;
        }
        var project = updateObj.project, environment = updateObj.environment;
        var validatedProject = typeof project === 'string' ? [Number(project)] : project;
        var validatedEnvironment = typeof environment === 'string' ? [environment] : environment;
        try {
            var localStorageKey = globalSelectionHeader_1.LOCAL_STORAGE_KEY + ":" + this.organization.slug;
            var dataToSave = {
                projects: validatedProject || this.selection.projects,
                environments: validatedEnvironment || this.selection.environments,
            };
            localStorage_1.default.setItem(localStorageKey, JSON.stringify(dataToSave));
        }
        catch (ex) {
            // Do nothing
        }
    },
};
var GlobalSelectionStore = reflux_1.default.createStore(storeConfig);
exports.default = GlobalSelectionStore;
//# sourceMappingURL=globalSelectionStore.jsx.map