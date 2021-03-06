<%inherit file="base.mako"/>

<%block name="central_container">
  <h3>${_(u'Depósitos')}</h3>
  <div class="box box-primary collapsed-box">
    <div class="box-header with-border">
      <h3 class="box-title">${_('Filtros')}</h3>
      <span class="visible-md visible-lg">${ filter_string }</span>
      <div class="box-tools pull-right">
        <button type="button" class="btn btn-box-tool" data-widget="collapse"><i class="fa fa-plus"></i>
        </button>
      </div>
    </div>
    <div class="box-body">
      <form name="filter" action="${request.route_url('list_deposits')}" method="posts">
        <div class="form-group">
          <label>${_(u'ISSN')}</label>
            <input name="filter_issn" type="text" class="form-control" value="${filter_issn or ''}"></input>
        </div>
        <div class="form-group">
          <label>${_(u'Acrônimo do periódico')}</label>
            <input name="filter_journal_acronym" type="text" class="form-control" value="${filter_journal_acronym or ''}"></input>
        </div>
        <div class="form-group">
          <label>${_(u'Prefix')}</label>
            <input name="filter_prefix" type="text" class="form-control" value="${filter_prefix or ''}"></input>
        </div>
        <div class="form-group">
          <label>${_(u'Referências válidas')}</label>
            <select name="filter_has_valid_references" class="form-control">
              <option value="" ${'selected' if filter_has_valid_references == '' else ''}>${_(u'todos')}</option>
              <option value="True" ${'selected' if filter_has_valid_references == 'True' else ''}>True</option>
              <option value="False" ${'selected' if filter_has_valid_references == 'False' else ''}>False</option>
            </select>
        </div>
        <div class="form-group">
          <label>${_(u'Situação de submissão')}</label>
          <select name="filter_submission_status" class="form-control">
            <option value="" ${'selected' if filter_submission_status == '' else ''}>${_(u'todos')}</option>
            % for item in sorted(submission_status_to_template):
              <option value="${item}" ${'selected' if filter_submission_status == item else ''}>${item}</option>
            % endfor
          </select>
        </div>
        <div class="form-group">
          <label>${_(u'Situação de depósito')}</label>
          <select name="filter_feedback_status" class="form-control">
            <option value="" ${'selected' if filter_feedback_status == '' else ''}>${_(u'todos')}</option>
            % for item in sorted(feedback_status_to_template):
              <option value="${item}" ${'selected' if filter_feedback_status == item else ''}>${item}</option>
            % endfor
          </select>
        </div>
        <div class="form-group">
          <label>${_(u'Data de início de processo')}</label>
          <div class="input-group">
            <div class="input-group-addon">
              <i class="fa fa-calendar"></i>
            </div>
            <input class="form-control pull-right" name="filter_start_range" type="text">
          </div>
          <!-- /.input group -->
        </div>
        <div class="form-group pull-right">
          <button type="submit" class="btn btn-primary">${_(u'aplicar')}</button>
        </div>
      </form>
    </div>
  </div>
  <div class="box box-primary">
    <div class="box-header with-border">
      <h3 class="box-title">${_('Depósitos')}</h3>
      <div class="box-tools pull-right">
        <div class="has-feedback">
          <form name="query_by_id" action="${request.route_url('list_deposits')}" method="get">
            <div class="input-group">
              <input type="text" name="filter_pid_doi" class="form-control" placeholder="${_(u'pesquise por DOI ou PID')}">
              <span class="input-group-btn">
                <button type="submit" id="search-btn" class="btn btn-default btn-flat"><i class="fa fa-search"></i>
                </button>
              </span>
            </div>
          </form>
        </div>
      </div>
    </div>
    <div class="box-body">
      <div class="row">
        <%include file="paging.mako"/>
      </div>
      <table id="deposits" class="table table-bordered table-hover">
        <thead>
          <tr>
            <th class="visible-md visible-lg"></th>
            <th class="visible-md visible-lg">${_(u'início de processo')}</th>
            <th>${_(u'periódico')}</th>
            <th>${_(u'depósito')}</th>
            <th class="visible-md visible-lg">${_(u'prefixo')}</th>
            <th class="visible-md visible-lg">${_(u'referências válidas')}</th>
            <th>${_(u'situação de submissão')}</th>
            <th>${_(u'situação de depósito')}</th>
            <th class="visible-md visible-lg" width="200px">${_(u'funções')}</th>
          </tr>
        </thead>
        <tbody>
          % for ndx, item in enumerate(deposits):
            <tr>
              <td class="visible-md visible-lg">${offset+ndx+1}</td>
              <td class="visible-md visible-lg">${item.started_at.strftime('%Y-%m-%d %H:%M:%S')}</td>
              <td><span class="visible-md visible-lg">${item.journal}</span> (${item.journal_acronym.upper()}) (${item.issue_label})</td>
              <td><a href="${request.route_url('deposit')}?code=${item.code}">${item.code}</a></td>
              <td class="visible-md visible-lg">${item.prefix}</td>
              <td class="visible-md visible-lg">${item.has_submission_xml_valid_references}</td>
              <td>
                <span class="label label-${submission_status_to_template[item.submission_status or 'unknow'][0]}">${item.submission_status}</span>
              </td>
              <td>
                <span class="label label-${feedback_status_to_template[item.feedback_status or 'unknow'][0]}">${item.feedback_status or ''}</span>
              </td>
              <td class="visible-md visible-lg" width="200px">
              <a href="${request.route_url('deposit')}?code=${item.code}">
                <button type="button" class="btn btn-primary btn-sm"><i class="fa fa-folder-open"></i> ${_(u'detalhes')}</button>
              </a>
              % if item.is_pending is True:
                <a href="#">
                  <button type="button" class="btn btn-primary btn-sm disabled"><i class="fa fa-cloud-upload"></i> ${_(u'resubmeter')}</button>
                </a>
              % else:
                <a href="${request.route_url('deposit_post')}?pids=${item.pid}">
                  <button type="button" class="btn btn-primary btn-sm"><i class="fa fa-cloud-upload"></i> ${_(u'resubmeter')}</button>
                </a>
              % endif
              </td>
            </tr>
            % endfor
        </tbody>
      </table>
      <div class="row">
        <%include file="paging.mako"/>
      </div>
    </div>
  </div>
</%block>

<%block name="footer_js">
<script type="text/javascript">
  $('input[name="filter_start_range"]').daterangepicker(
{
    locale: {
      format: 'MM/DD/YYYY'
    },
    startDate: '${filter_from_date}',
    endDate: '${filter_to_date}'
});
</script>
</%block>