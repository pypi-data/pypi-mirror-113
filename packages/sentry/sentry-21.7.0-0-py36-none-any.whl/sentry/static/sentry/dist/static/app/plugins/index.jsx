Object.defineProperty(exports, "__esModule", { value: true });
exports.registry = exports.DefaultIssuePlugin = exports.BasePlugin = void 0;
var tslib_1 = require("tslib");
var basePlugin_1 = tslib_1.__importDefault(require("app/plugins/basePlugin"));
exports.BasePlugin = basePlugin_1.default;
var defaultIssuePlugin_1 = tslib_1.__importDefault(require("app/plugins/defaultIssuePlugin"));
exports.DefaultIssuePlugin = defaultIssuePlugin_1.default;
var registry_1 = tslib_1.__importDefault(require("app/plugins/registry"));
var sessionstack_1 = tslib_1.__importDefault(require("./sessionstack/contexts/sessionstack"));
var jira_1 = tslib_1.__importDefault(require("./jira"));
var sessionstack_2 = tslib_1.__importDefault(require("./sessionstack"));
var contexts = {};
var registry = new registry_1.default();
exports.registry = registry;
// Register legacy plugins
// Sessionstack
registry.add('sessionstack', sessionstack_2.default);
contexts.sessionstack = sessionstack_1.default;
// Jira
registry.add('jira', jira_1.default);
var add = registry.add.bind(registry);
var get = registry.get.bind(registry);
var isLoaded = registry.isLoaded.bind(registry);
var load = registry.load.bind(registry);
exports.default = {
    BasePlugin: basePlugin_1.default,
    DefaultIssuePlugin: defaultIssuePlugin_1.default,
    add: add,
    addContext: function (id, component) {
        contexts[id] = component;
    },
    contexts: contexts,
    get: get,
    isLoaded: isLoaded,
    load: load,
};
//# sourceMappingURL=index.jsx.map