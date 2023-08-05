Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var broadcasts_1 = require("app/actionCreators/broadcasts");
var demoModeGate_1 = tslib_1.__importDefault(require("app/components/acl/demoModeGate"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var broadcastSdkUpdates_1 = tslib_1.__importDefault(require("app/components/sidebar/broadcastSdkUpdates"));
var sidebarItem_1 = tslib_1.__importDefault(require("app/components/sidebar/sidebarItem"));
var sidebarPanel_1 = tslib_1.__importDefault(require("app/components/sidebar/sidebarPanel"));
var sidebarPanelEmpty_1 = tslib_1.__importDefault(require("app/components/sidebar/sidebarPanelEmpty"));
var sidebarPanelItem_1 = tslib_1.__importDefault(require("app/components/sidebar/sidebarPanelItem"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var types_1 = require("./types");
var MARK_SEEN_DELAY = 1000;
var POLLER_DELAY = 600000; // 10 minute poll (60 * 10 * 1000)
var Broadcasts = /** @class */ (function (_super) {
    tslib_1.__extends(Broadcasts, _super);
    function Broadcasts() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            broadcasts: [],
            loading: true,
            error: false,
        };
        _this.poller = null;
        _this.timer = null;
        _this.fetchData = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var data, _a;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        if (this.poller) {
                            this.stopPoll();
                        }
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, broadcasts_1.getAllBroadcasts(this.props.api, this.props.organization.slug)];
                    case 2:
                        data = _b.sent();
                        this.setState({ loading: false, broadcasts: data || [] });
                        return [3 /*break*/, 4];
                    case 3:
                        _a = _b.sent();
                        this.setState({ loading: false, error: true });
                        return [3 /*break*/, 4];
                    case 4:
                        this.startPoll();
                        return [2 /*return*/];
                }
            });
        }); };
        /**
         * If tab/window loses visibility (note: this is different than focus), stop
         * polling for broadcasts data, otherwise, if it gains visibility, start
         * polling again.
         */
        _this.handleVisibilityChange = function () { return (document.hidden ? _this.stopPoll() : _this.startPoll()); };
        _this.handleShowPanel = function () {
            _this.timer = window.setTimeout(_this.markSeen, MARK_SEEN_DELAY);
            _this.props.onShowPanel();
        };
        _this.markSeen = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var unseenBroadcastIds;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        unseenBroadcastIds = this.unseenIds;
                        if (unseenBroadcastIds.length === 0) {
                            return [2 /*return*/];
                        }
                        return [4 /*yield*/, broadcasts_1.markBroadcastsAsSeen(this.props.api, unseenBroadcastIds)];
                    case 1:
                        _a.sent();
                        this.setState(function (state) { return ({
                            broadcasts: state.broadcasts.map(function (item) { return (tslib_1.__assign(tslib_1.__assign({}, item), { hasSeen: true })); }),
                        }); });
                        return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    Broadcasts.prototype.componentDidMount = function () {
        this.fetchData();
        document.addEventListener('visibilitychange', this.handleVisibilityChange);
    };
    Broadcasts.prototype.componentWillUnmount = function () {
        if (this.timer) {
            window.clearTimeout(this.timer);
            this.timer = null;
        }
        if (this.poller) {
            this.stopPoll();
        }
        document.removeEventListener('visibilitychange', this.handleVisibilityChange);
    };
    Broadcasts.prototype.startPoll = function () {
        this.poller = window.setTimeout(this.fetchData, POLLER_DELAY);
    };
    Broadcasts.prototype.stopPoll = function () {
        if (this.poller) {
            window.clearTimeout(this.poller);
            this.poller = null;
        }
    };
    Object.defineProperty(Broadcasts.prototype, "unseenIds", {
        get: function () {
            return this.state.broadcasts
                ? this.state.broadcasts.filter(function (item) { return !item.hasSeen; }).map(function (item) { return item.id; })
                : [];
        },
        enumerable: false,
        configurable: true
    });
    Broadcasts.prototype.render = function () {
        var _a = this.props, orientation = _a.orientation, collapsed = _a.collapsed, currentPanel = _a.currentPanel, hidePanel = _a.hidePanel;
        var _b = this.state, broadcasts = _b.broadcasts, loading = _b.loading;
        var unseenPosts = this.unseenIds;
        return (<demoModeGate_1.default>
        <react_1.Fragment>
          <sidebarItem_1.default data-test-id="sidebar-broadcasts" orientation={orientation} collapsed={collapsed} active={currentPanel === types_1.SidebarPanelKey.Broadcasts} badge={unseenPosts.length} icon={<icons_1.IconBroadcast size="md"/>} label={locale_1.t("What's new")} onClick={this.handleShowPanel} id="broadcasts"/>

          {currentPanel === types_1.SidebarPanelKey.Broadcasts && (<sidebarPanel_1.default data-test-id="sidebar-broadcasts-panel" orientation={orientation} collapsed={collapsed} title={locale_1.t("What's new in Sentry")} hidePanel={hidePanel}>
              <broadcastSdkUpdates_1.default />
              {loading ? (<loadingIndicator_1.default />) : broadcasts.length === 0 ? (<sidebarPanelEmpty_1.default>
                  {locale_1.t('No recent updates from the Sentry team.')}
                </sidebarPanelEmpty_1.default>) : (broadcasts.map(function (item) { return (<sidebarPanelItem_1.default key={item.id} hasSeen={item.hasSeen} title={item.title} message={item.message} link={item.link} cta={item.cta}/>); }))}
            </sidebarPanel_1.default>)}
        </react_1.Fragment>
      </demoModeGate_1.default>);
    };
    return Broadcasts;
}(react_1.Component));
exports.default = withApi_1.default(Broadcasts);
//# sourceMappingURL=broadcasts.jsx.map