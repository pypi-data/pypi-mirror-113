Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var reflux_1 = tslib_1.__importDefault(require("reflux"));
var environmentActions_1 = tslib_1.__importDefault(require("app/actions/environmentActions"));
var environment_1 = require("app/utils/environment");
var storeConfig = {
    state: {
        environments: null,
        error: null,
    },
    init: function () {
        this.state = { environments: null, error: null };
        this.listenTo(environmentActions_1.default.fetchEnvironments, this.onFetchEnvironments);
        this.listenTo(environmentActions_1.default.fetchEnvironmentsSuccess, this.onFetchEnvironmentsSuccess);
        this.listenTo(environmentActions_1.default.fetchEnvironmentsError, this.onFetchEnvironmentsError);
    },
    makeEnvironment: function (item) {
        return {
            id: item.id,
            name: item.name,
            get displayName() {
                return environment_1.getDisplayName(item);
            },
            get urlRoutingName() {
                return environment_1.getUrlRoutingName(item);
            },
        };
    },
    onFetchEnvironments: function () {
        this.state = { environments: null, error: null };
        this.trigger(this.state);
    },
    onFetchEnvironmentsSuccess: function (environments) {
        this.state = { error: null, environments: environments.map(this.makeEnvironment) };
        this.trigger(this.state);
    },
    onFetchEnvironmentsError: function (error) {
        this.state = { error: error, environments: null };
        this.trigger(this.state);
    },
    get: function () {
        return this.state;
    },
};
var OrganizationEnvironmentsStore = reflux_1.default.createStore(storeConfig);
exports.default = OrganizationEnvironmentsStore;
//# sourceMappingURL=organizationEnvironmentsStore.jsx.map