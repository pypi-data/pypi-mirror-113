Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var reflux_1 = tslib_1.__importDefault(require("reflux"));
var teamActions_1 = tslib_1.__importDefault(require("app/actions/teamActions"));
var teamStoreConfig = {
    initialized: false,
    state: [],
    init: function () {
        this.state = [];
        this.listenTo(teamActions_1.default.createTeamSuccess, this.onCreateSuccess);
        this.listenTo(teamActions_1.default.fetchDetailsSuccess, this.onUpdateSuccess);
        this.listenTo(teamActions_1.default.loadTeams, this.loadInitialData);
        this.listenTo(teamActions_1.default.removeTeamSuccess, this.onRemoveSuccess);
        this.listenTo(teamActions_1.default.updateSuccess, this.onUpdateSuccess);
    },
    reset: function () {
        this.state = [];
    },
    loadInitialData: function (items) {
        this.initialized = true;
        this.state = items;
        this.trigger(new Set(items.map(function (item) { return item.id; })));
    },
    onUpdateSuccess: function (itemId, response) {
        if (!response) {
            return;
        }
        var item = this.getBySlug(itemId);
        if (!item) {
            this.state.push(response);
            this.trigger(new Set([itemId]));
            return;
        }
        // Slug was changed
        // Note: This is the proper way to handle slug changes but unfortunately not all of our
        // components use stores correctly. To be safe reload browser :((
        if (response.slug !== itemId) {
            // Remove old team
            this.state = this.state.filter(function (_a) {
                var slug = _a.slug;
                return slug !== itemId;
            });
            // Add team w/ updated slug
            this.state.push(response);
            this.trigger(new Set([response.slug]));
            return;
        }
        var nextState = tslib_1.__spreadArray([], tslib_1.__read(this.state));
        var index = nextState.findIndex(function (team) { return team.slug === response.slug; });
        nextState[index] = response;
        this.state = nextState;
        this.trigger(new Set([itemId]));
    },
    onRemoveSuccess: function (slug) {
        this.loadInitialData(this.state.filter(function (team) { return team.slug !== slug; }));
    },
    onCreateSuccess: function (team) {
        this.loadInitialData(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(this.state)), [team]));
    },
    getById: function (id) {
        return this.state.find(function (item) { return item.id.toString() === id.toString(); }) || null;
    },
    getBySlug: function (slug) {
        return this.state.find(function (item) { return item.slug === slug; }) || null;
    },
    getActive: function () {
        return this.state.filter(function (item) { return item.isMember; });
    },
    getAll: function () {
        return this.state;
    },
};
var TeamStore = reflux_1.default.createStore(teamStoreConfig);
exports.default = TeamStore;
//# sourceMappingURL=teamStore.jsx.map