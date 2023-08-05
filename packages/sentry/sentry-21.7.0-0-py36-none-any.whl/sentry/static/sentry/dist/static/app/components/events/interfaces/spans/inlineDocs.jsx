Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var projects_1 = require("app/actionCreators/projects");
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var locale_1 = require("app/locale");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var InlineDocs = /** @class */ (function (_super) {
    tslib_1.__extends(InlineDocs, _super);
    function InlineDocs() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            html: undefined,
            link: undefined,
        };
        _this.fetchData = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, platform, api, orgSlug, projectSlug, tracingPlatform, _b, html, link, error_1;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, platform = _a.platform, api = _a.api, orgSlug = _a.orgSlug, projectSlug = _a.projectSlug;
                        if (!platform) {
                            return [2 /*return*/];
                        }
                        this.setState({ loading: true });
                        switch (platform) {
                            case 'sentry.python': {
                                tracingPlatform = 'python-tracing';
                                break;
                            }
                            case 'sentry.javascript.node': {
                                tracingPlatform = 'node-tracing';
                                break;
                            }
                            default: {
                                this.setState({ loading: false });
                                return [2 /*return*/];
                            }
                        }
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, projects_1.loadDocs(api, orgSlug, projectSlug, tracingPlatform)];
                    case 2:
                        _b = _c.sent(), html = _b.html, link = _b.link;
                        this.setState({ html: html, link: link });
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _c.sent();
                        Sentry.captureException(error_1);
                        this.setState({ html: undefined, link: undefined });
                        return [3 /*break*/, 4];
                    case 4:
                        this.setState({ loading: false });
                        return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    InlineDocs.prototype.componentDidMount = function () {
        this.fetchData();
    };
    InlineDocs.prototype.render = function () {
        var platform = this.props.platform;
        if (!platform) {
            return null;
        }
        if (this.state.loading) {
            return (<div>
          <loadingIndicator_1.default />
        </div>);
        }
        if (this.state.html) {
            return (<div>
          <h4>{locale_1.t('Requires Manual Instrumentation')}</h4>
          <DocumentationWrapper dangerouslySetInnerHTML={{ __html: this.state.html }}/>
          <p>
            {locale_1.tct("For in-depth instructions on setting up tracing, view [docLink:our documentation].", {
                    docLink: <a href={this.state.link}/>,
                })}
          </p>
        </div>);
        }
        return (<div>
        <h4>{locale_1.t('Requires Manual Instrumentation')}</h4>
        <p>
          {locale_1.tct("To manually instrument certain regions of your code, view [docLink:our documentation].", {
                docLink: (<a href="https://docs.sentry.io/product/performance/getting-started/"/>),
            })}
        </p>
      </div>);
    };
    return InlineDocs;
}(react_1.Component));
var DocumentationWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  p {\n    line-height: 1.5;\n  }\n  pre {\n    word-break: break-all;\n    white-space: pre-wrap;\n  }\n"], ["\n  p {\n    line-height: 1.5;\n  }\n  pre {\n    word-break: break-all;\n    white-space: pre-wrap;\n  }\n"])));
exports.default = withApi_1.default(InlineDocs);
var templateObject_1;
//# sourceMappingURL=inlineDocs.jsx.map