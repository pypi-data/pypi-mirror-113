Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var lightWeightNoProjectMessage_1 = tslib_1.__importDefault(require("app/components/lightWeightNoProjectMessage"));
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var locale_1 = require("app/locale");
var organization_1 = require("app/styles/organization");
var eventView_1 = tslib_1.__importDefault(require("app/utils/discover/eventView"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var content_1 = tslib_1.__importDefault(require("./content"));
var EventDetails = /** @class */ (function (_super) {
    tslib_1.__extends(EventDetails, _super);
    function EventDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getEventSlug = function () {
            var eventSlug = _this.props.params.eventSlug;
            if (typeof eventSlug === 'string') {
                return eventSlug.trim();
            }
            return '';
        };
        _this.getEventView = function () {
            var location = _this.props.location;
            return eventView_1.default.fromLocation(location);
        };
        _this.getDocumentTitle = function (name) {
            return typeof name === 'string' && String(name).trim().length > 0
                ? [String(name).trim(), locale_1.t('Discover')]
                : [locale_1.t('Discover')];
        };
        return _this;
    }
    EventDetails.prototype.render = function () {
        var _a = this.props, organization = _a.organization, location = _a.location, params = _a.params;
        var eventView = this.getEventView();
        var eventSlug = this.getEventSlug();
        var documentTitle = this.getDocumentTitle(eventView.name).join(' - ');
        var projectSlug = eventSlug.split(':')[0];
        return (<sentryDocumentTitle_1.default title={documentTitle} orgSlug={organization.slug} projectSlug={projectSlug}>
        <StyledPageContent>
          <lightWeightNoProjectMessage_1.default organization={organization}>
            <content_1.default organization={organization} location={location} params={params} eventView={eventView} eventSlug={eventSlug}/>
          </lightWeightNoProjectMessage_1.default>
        </StyledPageContent>
      </sentryDocumentTitle_1.default>);
    };
    return EventDetails;
}(react_1.Component));
exports.default = withOrganization_1.default(EventDetails);
var StyledPageContent = styled_1.default(organization_1.PageContent)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
var templateObject_1;
//# sourceMappingURL=index.jsx.map