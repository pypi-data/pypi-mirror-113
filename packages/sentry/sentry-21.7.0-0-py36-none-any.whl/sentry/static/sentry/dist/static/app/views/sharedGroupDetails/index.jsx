Object.defineProperty(exports, "__esModule", { value: true });
exports.SharedGroupDetails = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_document_title_1 = tslib_1.__importDefault(require("react-document-title"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var notFound_1 = tslib_1.__importDefault(require("app/components/errors/notFound"));
var eventEntries_1 = require("app/components/events/eventEntries");
var footer_1 = tslib_1.__importDefault(require("app/components/footer"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var locale_1 = require("app/locale");
var sentryTypes_1 = tslib_1.__importDefault(require("app/sentryTypes"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var sharedGroupHeader_1 = tslib_1.__importDefault(require("./sharedGroupHeader"));
var SharedGroupDetails = /** @class */ (function (_super) {
    tslib_1.__extends(SharedGroupDetails, _super);
    function SharedGroupDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getInitialState();
        _this.handleRetry = function () {
            _this.setState(_this.getInitialState());
            _this.fetchData();
        };
        return _this;
    }
    SharedGroupDetails.prototype.getInitialState = function () {
        return {
            group: null,
            loading: true,
            error: false,
        };
    };
    SharedGroupDetails.prototype.getChildContext = function () {
        return {
            group: this.state.group,
        };
    };
    SharedGroupDetails.prototype.componentWillMount = function () {
        document.body.classList.add('shared-group');
    };
    SharedGroupDetails.prototype.componentDidMount = function () {
        this.fetchData();
    };
    SharedGroupDetails.prototype.componentWillUnmount = function () {
        document.body.classList.remove('shared-group');
    };
    SharedGroupDetails.prototype.fetchData = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, params, api, shareId, group, _b;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, params = _a.params, api = _a.api;
                        shareId = params.shareId;
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/shared/issues/" + shareId + "/")];
                    case 2:
                        group = _c.sent();
                        this.setState({ loading: false, group: group });
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        this.setState({ loading: false, error: true });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    SharedGroupDetails.prototype.getTitle = function () {
        var group = this.state.group;
        if (group) {
            return group.title;
        }
        return 'Sentry';
    };
    SharedGroupDetails.prototype.render = function () {
        var _a = this.state, group = _a.group, loading = _a.loading, error = _a.error;
        if (loading) {
            return <loadingIndicator_1.default />;
        }
        if (!group) {
            return <notFound_1.default />;
        }
        if (error) {
            return <loadingError_1.default onRetry={this.handleRetry}/>;
        }
        var _b = this.props, location = _b.location, api = _b.api;
        var permalink = group.permalink, latestEvent = group.latestEvent, project = group.project;
        var title = this.getTitle();
        return (<react_document_title_1.default title={title}>
        <div className="app">
          <div className="pattern-bg"/>
          <div className="container">
            <div className="box box-modal">
              <div className="box-header">
                <link_1.default className="logo" to="/">
                  <span className="icon-sentry-logo-full"/>
                </link_1.default>
                {permalink && (<link_1.default className="details" to={permalink}>
                    {locale_1.t('Details')}
                  </link_1.default>)}
              </div>
              <div className="content">
                <sharedGroupHeader_1.default group={group}/>
                <Container className="group-overview event-details-container">
                  <eventEntries_1.BorderlessEventEntries location={location} organization={project.organization} group={group} event={latestEvent} project={project} api={api} isBorderless isShare/>
                </Container>
                <footer_1.default />
              </div>
            </div>
          </div>
        </div>
      </react_document_title_1.default>);
    };
    SharedGroupDetails.childContextTypes = {
        group: sentryTypes_1.default.Group,
    };
    return SharedGroupDetails;
}(react_1.Component));
exports.SharedGroupDetails = SharedGroupDetails;
var Container = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: 0 ", ";\n"], ["\n  padding: 0 ", ";\n"])), space_1.default(4));
exports.default = withApi_1.default(SharedGroupDetails);
var templateObject_1;
//# sourceMappingURL=index.jsx.map