Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var reflux_1 = tslib_1.__importDefault(require("reflux"));
var sidebarPanelActions_1 = tslib_1.__importDefault(require("../actions/sidebarPanelActions"));
var sidebarPanelStoreConfig = {
    activePanel: '',
    init: function () {
        this.listenTo(sidebarPanelActions_1.default.activatePanel, this.onActivatePanel);
        this.listenTo(sidebarPanelActions_1.default.hidePanel, this.onHidePanel);
        this.listenTo(sidebarPanelActions_1.default.togglePanel, this.onTogglePanel);
    },
    onActivatePanel: function (panel) {
        this.activePanel = panel;
        this.trigger(this.activePanel);
    },
    onTogglePanel: function (panel) {
        if (this.activePanel === panel) {
            this.onHidePanel();
        }
        else {
            this.onActivatePanel(panel);
        }
    },
    onHidePanel: function () {
        this.activePanel = '';
        this.trigger(this.activePanel);
    },
};
/**
 * This store is used to hold local user preferences
 * Side-effects (like reading/writing to cookies) are done in associated actionCreators
 */
var SidebarPanelStore = reflux_1.default.createStore(sidebarPanelStoreConfig);
exports.default = SidebarPanelStore;
//# sourceMappingURL=sidebarPanelStore.jsx.map