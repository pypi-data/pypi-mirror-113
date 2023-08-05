Object.defineProperty(exports, "__esModule", { value: true });
exports.modalCss = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_2 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var utils_1 = require("app/components/events/contexts/utils");
var notAvailable_1 = tslib_1.__importDefault(require("app/components/notAvailable"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var imageVisualization_1 = tslib_1.__importDefault(require("./imageVisualization"));
function Modal(_a) {
    var eventAttachment = _a.eventAttachment, orgSlug = _a.orgSlug, projectSlug = _a.projectSlug, Header = _a.Header, Body = _a.Body, Footer = _a.Footer, event = _a.event, onDelete = _a.onDelete, downloadUrl = _a.downloadUrl;
    var dateCreated = eventAttachment.dateCreated, name = eventAttachment.name, size = eventAttachment.size, mimetype = eventAttachment.mimetype, type = eventAttachment.type;
    return (<react_1.Fragment>
      <Header closeButton>
        <Title>
          {locale_1.t('Screenshot')}
          <FileName>
            {name ? name.split("." + name.split('.').pop())[0] : locale_1.t('Unknown')}
          </FileName>
        </Title>
      </Header>
      <Body>
        <GeralInfo>
          <Label coloredBg>{locale_1.t('Date Created')}</Label>
          <Value coloredBg>
            {dateCreated ? (<react_1.Fragment>
                <dateTime_1.default date={getDynamicText_1.default({
                value: dateCreated,
                fixed: new Date(1508208080000),
            })}/>
                {utils_1.getRelativeTimeFromEventDateCreated(event.dateCreated, dateCreated, false)}
              </react_1.Fragment>) : (<notAvailable_1.default />)}
          </Value>

          <Label>{locale_1.t('Name')}</Label>
          <Value>{name !== null && name !== void 0 ? name : <notAvailable_1.default />}</Value>

          <Label coloredBg>{locale_1.t('Size')}</Label>
          <Value coloredBg>{size !== null && size !== void 0 ? size : <notAvailable_1.default />}</Value>

          <Label>{locale_1.t('Mimetype')}</Label>
          <Value>{mimetype !== null && mimetype !== void 0 ? mimetype : <notAvailable_1.default />}</Value>

          <Label coloredBg>{locale_1.t('Type')}</Label>
          <Value coloredBg>{type !== null && type !== void 0 ? type : <notAvailable_1.default />}</Value>
        </GeralInfo>

        <StyledImageVisualization attachment={eventAttachment} orgId={orgSlug} projectId={projectSlug} event={event}/>
      </Body>
      <Footer>
        <buttonBar_1.default gap={1}>
          <confirm_1.default confirmText={locale_1.t('Delete')} header={locale_1.t('Screenshots help identify what the user saw when the event happened')} message={locale_1.t('Are you sure you wish to delete this screenshot?')} priority="danger" onConfirm={onDelete}>
            <button_1.default priority="danger">{locale_1.t('Delete')}</button_1.default>
          </confirm_1.default>
          <button_1.default href={downloadUrl}>{locale_1.t('Download')}</button_1.default>
        </buttonBar_1.default>
      </Footer>
    </react_1.Fragment>);
}
exports.default = Modal;
var Title = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n  max-width: calc(100% - 40px);\n  word-break: break-all;\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n  max-width: calc(100% - 40px);\n  word-break: break-all;\n"])), space_1.default(1), function (p) { return p.theme.fontSizeExtraLarge; });
var FileName = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-family: ", ";\n"], ["\n  font-family: ", ";\n"])), function (p) { return p.theme.text.familyMono; });
var GeralInfo = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  margin-bottom: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  margin-bottom: ", ";\n"])), space_1.default(3));
var Label = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  padding: ", " ", " ", " ", ";\n  ", "\n"], ["\n  color: ", ";\n  padding: ", " ", " ", " ", ";\n  ", "\n"])), function (p) { return p.theme.textColor; }, space_1.default(1), space_1.default(1.5), space_1.default(1), space_1.default(1), function (p) { return p.coloredBg && "background-color: " + p.theme.backgroundSecondary + ";"; });
var Value = styled_1.default(Label)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  white-space: pre-wrap;\n  word-break: break-all;\n  color: ", ";\n  padding: ", ";\n  font-family: ", ";\n  ", "\n"], ["\n  white-space: pre-wrap;\n  word-break: break-all;\n  color: ", ";\n  padding: ", ";\n  font-family: ", ";\n  ", "\n"])), function (p) { return p.theme.subText; }, space_1.default(1), function (p) { return p.theme.text.familyMono; }, function (p) { return p.coloredBg && "background-color: " + p.theme.backgroundSecondary + ";"; });
var StyledImageVisualization = styled_1.default(imageVisualization_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  img {\n    border-radius: ", ";\n  }\n"], ["\n  img {\n    border-radius: ", ";\n  }\n"])), function (p) { return p.theme.borderRadius; });
exports.modalCss = react_2.css(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  width: auto;\n  height: 100%;\n  max-width: 100%;\n"], ["\n  width: auto;\n  height: 100%;\n  max-width: 100%;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=modal.jsx.map