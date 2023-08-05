Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var list_1 = tslib_1.__importDefault(require("app/components/list"));
var listItem_1 = tslib_1.__importDefault(require("app/components/list/listItem"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var numberField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/numberField"));
var radioField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/radioField"));
var impacts = [
    locale_1.tct("[strong:Quota applies.] Every event you choose to reprocess counts against your plan's quota. Rate limits and spike protection do not apply.", { strong: <strong /> }),
    locale_1.tct('[strong:Attachment storage required.] If your events come from minidumps or unreal crash reports, you must have [link:attachment storage] enabled.', {
        strong: <strong />,
        link: (<externalLink_1.default href="https://docs.sentry.io/platforms/native/enriching-events/attachments/#crash-reports-and-privacy"/>),
    }),
    locale_1.t('Please wait one hour after upload before attempting to reprocess missing debug files.'),
];
var remainingEventsChoices = [
    ['keep', locale_1.t('Keep')],
    ['delete', locale_1.t('Delete')],
];
var ReprocessingEventModal = /** @class */ (function (_super) {
    tslib_1.__extends(ReprocessingEventModal, _super);
    function ReprocessingEventModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = { maxEvents: undefined };
        _this.handleSuccess = function () {
            var closeModal = _this.props.closeModal;
            closeModal();
            window.location.reload();
        };
        _this.handleMaxEventsChange = function (maxEvents) {
            _this.setState({ maxEvents: Number(maxEvents) || undefined });
        };
        return _this;
    }
    ReprocessingEventModal.prototype.handleError = function () {
        indicator_1.addErrorMessage(locale_1.t('Failed to reprocess. Please check your input.'));
    };
    ReprocessingEventModal.prototype.render = function () {
        var _a = this.props, organization = _a.organization, Header = _a.Header, Body = _a.Body, closeModal = _a.closeModal, groupId = _a.groupId;
        var maxEvents = this.state.maxEvents;
        var orgSlug = organization.slug;
        var endpoint = "/organizations/" + orgSlug + "/issues/" + groupId + "/reprocessing/";
        var title = locale_1.t('Reprocess Events');
        return (<react_1.Fragment>
        <Header closeButton>{title}</Header>
        <Body>
          <Introduction>
            {locale_1.t('Reprocessing applies new debug files and grouping enhancements to this Issue. Please consider these impacts:')}
          </Introduction>
          <StyledList symbol="bullet">
            {impacts.map(function (impact, index) { return (<listItem_1.default key={index}>{impact}</listItem_1.default>); })}
          </StyledList>
          <Introduction>
            {locale_1.tct('For more information, please refer to [link:the documentation.]', {
                link: (<externalLink_1.default href="https://docs.sentry.io/product/error-monitoring/reprocessing/"/>),
            })}
          </Introduction>
          <form_1.default submitLabel={title} apiEndpoint={endpoint} apiMethod="POST" initialData={{ maxEvents: undefined, remainingEvents: 'keep' }} onSubmitSuccess={this.handleSuccess} onSubmitError={this.handleError} onCancel={closeModal} footerClass="modal-footer">
            <numberField_1.default name="maxEvents" label={locale_1.t('Number of events to be reprocessed')} help={locale_1.t('If you set a limit, we will reprocess your most recent events.')} placeholder={locale_1.t('Reprocess all events')} onChange={this.handleMaxEventsChange} min={1}/>

            <radioField_1.default orientInline label={locale_1.t('Remaining events')} help={locale_1.t('What to do with the events that are not reprocessed.')} name="remainingEvents" choices={remainingEventsChoices} disabled={maxEvents === undefined}/>
          </form_1.default>
        </Body>
      </react_1.Fragment>);
    };
    return ReprocessingEventModal;
}(react_1.Component));
exports.default = ReprocessingEventModal;
var Introduction = styled_1.default('p')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeLarge; });
var StyledList = styled_1.default(list_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  grid-gap: ", ";\n  margin-bottom: ", ";\n  font-size: ", ";\n"], ["\n  grid-gap: ", ";\n  margin-bottom: ", ";\n  font-size: ", ";\n"])), space_1.default(1), space_1.default(4), function (p) { return p.theme.fontSizeMedium; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=reprocessEventModal.jsx.map