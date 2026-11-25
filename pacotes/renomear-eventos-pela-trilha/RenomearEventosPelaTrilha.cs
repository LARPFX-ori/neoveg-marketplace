// Renomear eventos pela trilha: dá a cada evento o nome da trilha seguido de
// um número em ordem de tempo ("Vídeo 1 - 01", "Vídeo 1 - 02"...). Com eventos
// selecionados, só eles mudam. Licença: MIT OR Apache-2.0.

using System;
using System.Collections.Generic;
using ScriptPortal.Vegas;

public class EntryPoint
{
    public void FromVegas(Vegas vegas)
    {
        bool algumSelecionado = false;
        foreach (Track trilha in vegas.Project.Tracks)
            foreach (TrackEvent ev in trilha.Events)
                if (ev.Selected) algumSelecionado = true;

        foreach (Track trilha in vegas.Project.Tracks)
        {
            var eventos = new List<TrackEvent>();
            foreach (TrackEvent ev in trilha.Events)
                if (!algumSelecionado || ev.Selected) eventos.Add(ev);
            eventos.Sort((a, b) => a.Start.CompareTo(b.Start));
            string baseNome = string.IsNullOrWhiteSpace(trilha.Name)
                ? "Trilha " + (trilha.Index + 1)
                : trilha.Name.Trim();
            for (int i = 0; i < eventos.Count; i++)
                eventos[i].Name = baseNome + " - " + (i + 1).ToString("00");
        }
    }
}
