Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var eventDataSection_1 = tslib_1.__importDefault(require("app/components/events/eventDataSection"));
var lazyLoad_1 = tslib_1.__importDefault(require("app/components/lazyLoad"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var RRWebIntegration = /** @class */ (function (_super) {
    tslib_1.__extends(RRWebIntegration, _super);
    function RRWebIntegration() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    RRWebIntegration.prototype.getEndpoints = function () {
        var _a = this.props, orgId = _a.orgId, projectId = _a.projectId, event = _a.event;
        return [
            [
                'attachmentList',
                "/projects/" + orgId + "/" + projectId + "/events/" + event.id + "/attachments/",
                { query: { query: 'rrweb.json' } },
            ],
        ];
    };
    RRWebIntegration.prototype.renderLoading = function () {
        // hide loading indicator
        return null;
    };
    RRWebIntegration.prototype.renderBody = function () {
        var attachmentList = this.state.attachmentList;
        if (!(attachmentList === null || attachmentList === void 0 ? void 0 : attachmentList.length)) {
            return null;
        }
        var attachment = attachmentList[0];
        var _a = this.props, orgId = _a.orgId, projectId = _a.projectId, event = _a.event;
        return (<StyledEventDataSection type="context-replay" title={locale_1.t('Replay')}>
        <lazyLoad_1.default component={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('./rrwebReplayer')); }); }} url={"/api/0/projects/" + orgId + "/" + projectId + "/events/" + event.id + "/attachments/" + attachment.id + "/?download"}/>
      </StyledEventDataSection>);
    };
    return RRWebIntegration;
}(asyncComponent_1.default));
var StyledEventDataSection = styled_1.default(eventDataSection_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  overflow: hidden;\n  margin-bottom: ", ";\n"], ["\n  overflow: hidden;\n  margin-bottom: ", ";\n"])), space_1.default(3));
exports.default = RRWebIntegration;
var templateObject_1;
//# sourceMappingURL=rrwebIntegration.jsx.map